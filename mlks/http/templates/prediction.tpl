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
    <script>

        database = %(DATABASE)s;

        evaluationData = %(EVALUATION_DATA)s;

        titleTemplate = '<tr><th class="is-size-5" style="padding: 5px 10px;">Class</th><th class="is-size-5" style="padding: 5px 10px;">Prediction</th></tr>'

        classTemplate = '<tr>' +
            '<td class="is-size-6" style="border-bottom-width: 0px; padding: 5px 10px 0 10px;">%%(name)s</td>' +
            '<td class="is-size-5" style="border-bottom-width: 0px; padding: 5px 10px 0 10px;">%%(percent)s</td>' +
        '</tr>';
        classTemplateExtra = '<tr><td colspan="2" class="is-size-7" style="padding: 0 10px 5px 10px;">%%(more)s</td></tr>';

    </script>

    <h1 class="title"><span class="pictogram">%(ICON)s</span> %(MODEL_TYPE_TITLE)s prediction result</h1>
    <h2 class="subtitle">The analysed and classified %(MODEL_TYPE)s</h2>

    <h3 class="subtitle">Source image (%(EVALUATED_FILE_WEB_SIZE)s)</h3>
    <p><img class="bordered" src="%(EVALUATED_FILE_WEB)s" style="max-width: 100%%;"></p>
    <p>&nbsp;</p>

    <h3 class="subtitle">Predicted image (%(PREDICTION_CLASS)s - %(PREDICTION_ACCURACY)s%% - %(PREDICTION_TIME)ss)</h3>
    <p><img class="bordered" src="%(GRAPH_FILE_WEB)s" style="max-width: 100%%;"></p>
    <p>&nbsp;</p>

    <h3 class="subtitle">Prediction classes</h3>
    <p>In the order in which the model would classify the image.</p>
    <p>&nbsp;</p>
    <p>
        <a href="#" onclick="window.renewPredictionOverview(database, evaluationData, titleTemplate, classTemplate, classTemplateExtra, 'GB'); return false;">GB</a> -
        <a href="#" onclick="window.renewPredictionOverview(database, evaluationData, titleTemplate, classTemplate, classTemplateExtra, 'DE'); return false;">DE</a>
    <p/>
    <div class="table-container">
        <table class="table is-fullwidth is-hoverable" id="prediction-table"></table>
        <script>

            window.renewPredictionOverview(database, evaluationData, titleTemplate, classTemplate, classTemplateExtra, 'GB');

        </script>
    </div>
    <p>&nbsp;</p>

    <h3 class="subtitle">Picture upload form</h3>
    %(UPLOAD_FORM)s
    %(USED_MODEL)s
</div>

