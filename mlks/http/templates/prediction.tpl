<div class="container">
    <nav class="breadcrumb" aria-label="breadcrumbs">
        <ul>
            <li><a href="/">Overview</a></li>
            <li class="is-active"><a href="#" aria-current="page">Flower prediction</a></li>
        </ul>
    </nav>
</div>

<div class="container">
    <h1 class="title"><span class="pictogram">&#127803;</span> Flower prediction result</h1>
    <h2 class="subtitle">The analysed and classified flower</h2>

    <h3 class="subtitle">Source image (%(EVALUATED_FILE_WEB_SIZE)s)</h3>
    <p><img src="%(EVALUATED_FILE_WEB)s" style="max-width: 100%%;"></p>
    <h3 class="subtitle">Predicted image (%(PREDICTION_CLASS)s - %(PREDICTION_ACCURACY)s%%)</h3>
    <p><img src="%(GRAPH_FILE_WEB)s" style="max-width: 100%%;"></p>
    <h3 class="subtitle">Prediction classes</h3>
    <pre class="code">%(PREDICTION_OVERVIEW)s</pre>
    <p>&nbsp;</p>

    %(UPLOAD_FORM)s
</div>

