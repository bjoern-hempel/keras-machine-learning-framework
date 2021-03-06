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

        titleTemplate = '' +
            '<tr>' +
                '<th class="is-size-5 prediction-header-class">Class</th>' +
                '<th class="is-size-6 prediction-header-accuracy">Accuracy</th>' +
            '</tr>';

        classTemplate = '' +
            '<tr>' +
                '<td colspan="2" class="is-size-6 prediction-title %%(classes)s"><div style="float: right; margin-left: 10px;">%%(percent)s</div>%%(name)s</td>' +
            '</tr>';

        classTemplateExtra = '' +
            '<tr>' +
                '<td colspan="2" class="is-size-7 prediction-description">%%(more)s</td>' +
            '</tr>';

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
    <p id="language-switcher"><p/>
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

