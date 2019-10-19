<nav class="breadcrumb" aria-label="breadcrumbs">
    <ul>
        <li><a href="/">Overview</a></li>
        <li class="is-active"><a href="#" aria-current="page">Flower prediction</a></li>
    </ul>
</nav>

<div class="container">
    <h1 class="title">Flower prediction result</h1>
    <h2 class="subtitle">The analysed and classified flower</h2>

    <h3 class="subtitle">Source image</h3>
    <p><img src="%(evaluated_file_web)s" style="max-width: 100%%;"></p>
    <h3 class="subtitle">Predicted image (%(prediction_class)s - %(prediction_accuracy)s%%)</h3>
    <p><img src="%(graph_file_web)s" style="max-width: 100%%;"></p>
    <h3 class="subtitle">Prediction classes</h3>
    <pre class="code">%(prediction_overview)s</pre>
    <p>&nbsp;</p>

    %(upload_form)s
</div>

