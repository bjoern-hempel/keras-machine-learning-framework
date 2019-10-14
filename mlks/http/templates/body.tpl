<html>
    <head>
        <title>Keras Machine Learning Framework - Evaluation Form</title>
        <style>
            .waitdiv {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%%;
                height: 100%%;
                background-color: #fff;
                display: none;
            }
        </style>
        <script>
            window.pleaseWait = function () {
                document.getElementById("waitdiv").style.display = "block";
            }
        </script>
    </head>
    <body>
        <div class="waitdiv" id="waitdiv">%s</div>
        %s
    </body>
</html>