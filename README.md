

# Log Analysis Project - Udacity Full Stack Nanodegree

## Author - Ron Duran


## Project Instructions

### 1.  What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

#### Example:

```
"Princess Shellfish Marries Prince Handsome" — 1201 views
"Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
"Political Scandal Ends In Political Scandal" — 553 views
```

### 2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

#### Example:

```
Ursula La Multa — 2304 views
Rudolf von Treppenwitz — 1985 views
Markoff Chaney — 1723 views
Anonymous Contributor — 1023 views
```

### 3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer back to this lesson if you want to review the idea of HTTP status codes.)

#### Example:

```
July 29, 2016 — 2.5% errors
```
## Running the Reporting Tool

### Prior to runnning the tool, you will need to create some views in the database.  These views support the queries that are used by the Python code.


	create view v_log_top3 as
	select path, count(path) as views
	from log
	group by path
	order by views desc
	limit 3 offset 1;

	create view v_authors_slugs
	select slug, name
	from articles, authors
	where articles.author = authors.id;

	create view v_log_pathviews
	select path, count(path)
	from log
	group by path;

	create view v_author_slug_views
	select name, slug, views 
	from v_authors_slugs, v_log_pathviews
	where v_log_pathviews.path like ‘/article/‘ || v_authors_slugs.slug;

	View to get error count for each day:

	create view v_log_errorstatus_per_day as
	select date_trunc('day', time), count(*)
	from log
	where status not like '%200%'
	group by date_trunc('day', time)
	order by date_trunc('day', time);

	create view v_log_allstatus_per_day as
	select date_trunc('day', time), count(*)
	from log
	group by date_trunc('day', time)
	order by date_trunc('day', time);

	create view v_error_percent_per_day as
	select v1.date_trunc, round(100.0*v1.count/v2.count, 1) as percent
	from v_log_errorstatus_per_day as v1, v_log_allstatus_per_day as v2
	where v1.date_trunc = v2.date_trunc;

	create view v_high_error_dates as
	select to_char(v1.date_trunc, 'Month DD, YYYY'), v1.percent
	from v_error_percent_per_day as v1
	where v1.percent > 1.0
	group by v1.date_trunc, v1.percent
	order by v1.percent desc;


#### After creating the views you can run the report
```
python3 reporting_tool.py
```
## Solution Thought Process:
### Requirement 1
The top 3 articles should be the top 3 accessed in the log.  Since the path in the log table indicate which articles are being accessed, we can count the number of times each path occurs and sort them descending to get the most popular paths.  I ran the following query as a test:

	select path, count(path) as views
	from log
	group by path
	order by views desc
	limit 30;

The results showed that the root (/) path is the most accessed followed by the top 3 articles.  I created the v_log_top3 view to prepare the data for the final query.

In the articles table, the slug column contains the text we need to match in the log path. The following query uses our v_log_top3 view to get the article title and number of views by using the v_log_top3 view we created:

	select title, views
	from articles, v_log_top3
	where v_log_top3.path like 
	(‘/article/’  || articles.slug)
	order by num_views desc;

This gives us the results we need to create the report.



### Requirement 2

We need to know what articles have been written by which authors.  The logs don’t contain the title’s but as in the first requirement, they do have paths which contain the slugs that are in articles table.  Also, the articles don’t list the authors by name but use a foreign key on the author's id in the authors table.  

Creating the v_authors_slugs view allows us to get the slug and the name of the author.  I need the slug in order to search for it in the path of the log table.

In order to sum up the number of times an article has been accessed we can create a view that contains the number each path has been accessed so that when we match up the slug later with the path, we will be able to count them.  The v_log_pathviews view gives us this data.

We can combine the results from querying the previous two views that will allow us to have each article view count for each article.  The v_author_slug_views view is used to get data from both v_authors_slugs and v_log_pathviews.

Now all we need to do is to sum up the views for each author.  Here is the query we use in the reporting tool:

	select name, sum(views) as views
	from v_author_slug_views
	group by name
	order by views desc;

This gives us our names and views in order of popularity that we need for our report. 


### Requirement 3 

This requirement is simple in theory but presents some issues when run against a large database.  The aggregate functions and other string and math functions can take quite a while to return data and it took some trial and error to find a solution that was reasonably fast.

We need the number of errors for each day so we create a view that will give us a list of days along with the number of http status errors.  The view is v_log_errorstatus_per_day.

To find the percentage of all access status, we need the number of accesses for each day.  The view is similar to the one we created for the errors except we don't check the status since it is not needed for the count.  The view v_log_allstatus_per_day is created to provide this data.

Now we have the number of errors and the total number of accesses per day we can do the math needed to determine the percentage.  Multiplying the ratio of errorstatus/allstatus by 100.0 helps us in two ways.  It gives us a double precison number and also gives us a percentage that is easier to read.  Rounding the result to one decimal place fits our output requirement.  We create the v_error_percent_per_day view for this purpose.

The last thing we need to do is get the data for the report.  Instead of putting this query inside the reporting tool, I've created the v_high_error_dates view just for the fun of having the data available through a simple select query.
