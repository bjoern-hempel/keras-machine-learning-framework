<div class="container">
    <nav class="breadcrumb" aria-label="breadcrumbs">
        <ul>
            <li><a href="/">Overview</a></li>
            <li class="is-active"><a href="#" aria-current="page">%(MODEL_TYPE_TITLE)s prediction</a></li>
        </ul>
    </nav>

    <p>&nbsp;</p>
</div>

<div class="container">
    <h1 class="title"><span class="pictogram">%(ICON)s</span> %(MODEL_TYPE_TITLE)s prediction result</h1>
    <h2 class="subtitle">The analysed and classified %(MODEL_TYPE)s</h2>

    <h3 class="subtitle">Source image (%(EVALUATED_FILE_WEB_SIZE)s)</h3>
    <p><img class="bordered" src="%(EVALUATED_FILE_WEB)s" style="max-width: 100%%;"></p>
    <p>&nbsp;</p>

    <h3 class="subtitle">Predicted image (%(PREDICTION_CLASS)s - %(PREDICTION_ACCURACY)s%% - %(PREDICTION_TIME)ss)</h3>
    <p><img class="bordered" src="%(GRAPH_FILE_WEB)s" style="max-width: 100%%;"></p>
    <p>&nbsp;</p>

    <h3 class="subtitle">Prediction classes</h3>
    <div class="table-container">
        <table class="table is-fullwidth is-hoverable">
            %(PREDICTION_OVERVIEW)s
        </table>
    </div>
    <p>&nbsp;</p>

    <h3 class="subtitle">Picture upload form</h3>
    %(UPLOAD_FORM)s
    %(USED_MODEL)s
</div>

