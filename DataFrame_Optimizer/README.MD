<h1>Dataframe Optimizer</h1>
<p>This project is used to increase memory efficiency of dataframe and reduce resource consumption</p>

<h2>Download the file</h2>
<p>Get the copy of the module and start experimenting.</p>

<h3>Prerequisities</h3>
<p>The module was developed in python3 with only usage of python-pandas library.</p>

<h3></h3>
<p> Following Steps will suffice to run the module</p>
<pre>
<code>df_optimizer = DataframeOptimizer(source_df)</code>
</pre>


<p>To view memory print of the unoptimized/source dataframe.</p>
<pre>
<code>df_optimizer.get_memory_usage(source_df)</code>
</pre>

<p>Here, dataframe columns or series memory print can also be viewed.</p>
<pre>
<code>df_optimizer.get_memory_usage(source_df.column1)</code>
</pre>

<p>Individual column types(dtypes) memory usage can also be viewed as follow.</p>
<pre>
<code>df_optimizer.get_memory_usage_for_datatypes(source_df)</code>
</pre>

<p>Optimizing the dataframe can be done using:</p>
<pre>
<code>df_optimizer.optimize_dataframe()</code>
</pre>

<p>To get the optimized dataframe</p>
<pre>
<code>df_optimizer.get_optimized_dataframe()</code>
</pre>

<h2>Built With</h2>
<ul>
<li>Python3</li>
<li>python-pandas</li>
</ul>

<h2>Author</h2>
<ul>
<li><strong>Rohan Man Amatya</strong></li>
</ul>