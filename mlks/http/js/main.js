/** some configs */
window.max_size = 1024;

window.submitPicture = function () {
    /* show uploading info */
    document.getElementById('info-uploading').style.display = 'block';

    /* disable all form elements */
    document.querySelectorAll('#prediction-form button:not([data-ignore-disabling]), prediction-form input').forEach(function (entry) {
        entry.disabled = true;
    });

    /* disable all graphic file elements */
    document.querySelectorAll('.file .file-label').forEach(function (entry) {
        entry.className = entry.className.concat(' file-label-disabled');
    });

    /* continue uploading (true) */
    return true;
}

window.renewPredictionOverview = function(database, evaluationData, titleTemplate, classTemplate, classTemplateExtra) {
    let html = titleTemplate;
    let language = 'GB';

    for (let index in evaluationData['prediction_overview_array']) {
        let predictionItem = evaluationData['prediction_overview_array'][index];
        let className = predictionItem['class_name'];
        let percent = Math.round(predictionItem['predicted_value'] * 100 * 100) / 100;
        let classes = database['classes'];
        let categories = database['categories'];
        let name = className;

        console.log(classes);
        console.log(className);

        if (className in classes) {
            name = '<b>' + classes[className]['name'][language] + '</b>';
        }

        var predictionHtml = classTemplate.
            replace(/%\(name\)s/, name).
            replace(/%\(percent\)s/, percent + '%');

        if (className in classes) {
            let description = classes[className]['description'][language];

            description += '<br /><b>Wikipedia:</b> </b>' +
                '<a href="' + classes[className]['urls']['wikipedia'][language] + '" target="_blank">' +
                    classes[className]['urls']['wikipedia'][language] +
                '</a>'
            ;

            let categoriesCurrent = classes[className]['categories'];

            for (let categoryId in categoriesCurrent) {
                let categoryCurrent = categoriesCurrent[categoryId];
                description += '<br /><b>Category:</b> ' +
                    '<a href="' + categories[categoryCurrent]['urls']['wikipedia'][language] + '" target="_blank">' +
                        categories[categoryCurrent]['name'][language] +
                    '</a>'
                ;
            }

            predictionHtml += classTemplateExtra.
                replace(/%\(more\)s/, description);
        }

        html += predictionHtml
    }

    document.getElementById('prediction-table').innerHTML = html;
}

window.fileChange = function (e) {
    document.getElementById('predict-file-raw').value = '';
    document.getElementById('predict-file-name').value = '';

    let file = e.target.files[0];
    if (file.type != "image/jpeg" && file.type != "image/png") {
        document.getElementById('predict-file-source').value = '';
        alert('Please only select images in JPG- or PNG-format.');
    }

    let reader = new FileReader();
    reader.onload = function (readerEvent) {
        let image = new Image();
        image.onload = function (imageEvent) {
            let w = image.width;
            let h = image.height;

            if (w > h) {
                if (w > window.max_size) {
                    h *= window.max_size / w;
                    w = window.max_size;
                }
            } else {
                if (h > window.max_size) {
                    w *= window.max_size / h;
                    h = window.max_size;
                }
            }

            let canvas = document.createElement('canvas');
            canvas.width = w;
            canvas.height = h;
            canvas.getContext('2d').drawImage(image, 0, 0, w, h);

            let dataUrl;
            if (file.type == "image/jpeg") {
                dataUrl = canvas.toDataURL("image/jpeg", 0.8);
            } else {
                dataUrl = canvas.toDataURL("image/png");
            }

            document.getElementById('predict-file-raw').value = dataUrl;
            document.getElementById('predict-file-name').value = file.name;
        };
        image.src = readerEvent.target.result;
    };

    reader.readAsDataURL(file);
};

document.addEventListener("DOMContentLoaded", function(event) {
    let predictFileSource = document.getElementById('predict-file-source');

    if (predictFileSource !== null) {
        predictFileSource.addEventListener('change', window.fileChange, false);
    }
});