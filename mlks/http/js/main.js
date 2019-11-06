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
};

window.getFinalClassNameConfig = function(database, className, finalClassNameConfig = {}) {
    let classes = database['classes'];

    /* clone object */
    finalClassNameConfig = JSON.parse(JSON.stringify(finalClassNameConfig));

    /* the class name was not found */
    if (!(className in classes)) {
        return null;
    }

    /* Plural was found */
    if (('plural' in classes[className]) && (classes[className]['plural'] in classes)) {
        finalClassNameConfig['is-plural'] = classes[className]['plural'];

        if (!('original-class-name' in finalClassNameConfig)) {
            finalClassNameConfig['original-class-name'] = className;
        }

        return window.getFinalClassNameConfig(database, classes[className]['plural'], finalClassNameConfig);
    }

    /* Singular was found */
    if (('singular' in classes[className]) && (classes[className]['singular'] in classes)) {
        finalClassNameConfig['is-singular'] = classes[className]['singular'];

        if (!('original-class-name' in finalClassNameConfig)) {
            finalClassNameConfig['original-class-name'] = className;
        }

        return window.getFinalClassNameConfig(database, classes[className]['singular'], finalClassNameConfig);
    }

    /* Singular was found */
    if (('duplicate' in classes[className]) && (classes[className]['duplicate'] in classes)) {
        finalClassNameConfig['is-duplicate'] = classes[className]['duplicate'];

        if (!('original-class-name' in finalClassNameConfig)) {
            finalClassNameConfig['original-class-name'] = className;
        }

        return window.getFinalClassNameConfig(database, classes[className]['duplicate'], finalClassNameConfig);
    }

    let classesConfig = JSON.parse(JSON.stringify(classes[className]));

    finalClassNameConfig = Object.assign(classesConfig, finalClassNameConfig);

    return finalClassNameConfig;
}

window.getName = function(database, className, language) {
    let finalClassNameConfig = window.getFinalClassNameConfig(database, className);
    let name = className;
    let nameAdd = '';

    let translatePlural = {
        'GB': 'Plural of ',
        'DE': 'Mehrzahl von '
    };
    let translateSingular = {
        'GB': 'Singular of ',
        'DE': 'Einzahl von '
    };
    let translateDuplicate = {
        'GB': 'Duplicate of ',
        'DE': 'Dublette von '
    };
    let translateClassName = {
        'GB': 'Class name',
        'DE': 'Klassenname'
    };

    if (finalClassNameConfig === null) {
        if (name !== className) {
            nameAdd += nameAdd !== '' ? ' - ' : '';
            nameAdd += ' <span class="is-size-7">' + translateClassName[language] + ': "<b>' + className + '</b>"' + '</span>';
        }
        return '<b>' + name + '</b>' + nameAdd;
    }

    name = finalClassNameConfig['name'][language] === "" ? className : finalClassNameConfig['name'][language];
    nameAdd = '';

    if (finalClassNameConfig['is-plural'] || finalClassNameConfig['is-singular'] || finalClassNameConfig['is-duplicate']) {
        if (finalClassNameConfig['original-class-name']) {
            //nameAdd += nameAdd !== '' ? ' - ' : '';
            nameAdd += '<br /><span class="is-size-7">' + translateClassName[language] + ': "<b>' + className + '</b>"' + '</span>';
        } else {
            if (name !== className) {
                //nameAdd += nameAdd !== '' ? ' - ' : '';
                nameAdd += '<br /><span class="is-size-7">' + translateClassName[language] + ': "<b>' + className + '</b>"' + '</span>';
            }
        }
    } else {
        if (name !== className) {
            //nameAdd += nameAdd !== '' ? ' - ' : '';
            nameAdd += '<br /><span class="is-size-7">' + translateClassName[language] + ': "<b>' + className + '</b>"' + '</span>';
        }
    }
    if (finalClassNameConfig['is-plural']) {
        //nameAdd += nameAdd !== '' ? ', ' : '';
        nameAdd += '<br /><span class="is-size-7" style="color: red;">' + translatePlural[language] + '"<b>' + finalClassNameConfig['is-plural'] + '</b>"' + '</span>';
    }
    if (finalClassNameConfig['is-singular']) {
        //nameAdd += nameAdd !== '' ? ', ' : '';
        nameAdd += '<br /><span class="is-size-7" style="color: red;">' + translateSingular[language] + '"<b>' + finalClassNameConfig['is-singular'] + '</b>"' + '</span>';
    }
    if (finalClassNameConfig['is-duplicate']) {
        //nameAdd += nameAdd !== '' ? ', ' : '';
        nameAdd += '<br /><span class="is-size-7" style="color: red;">' + translateDuplicate[language] + '"<b>' + finalClassNameConfig['is-duplicate'] + '</b>"' + '</span>';
    }

    return '<b>' + name + '</b>' + nameAdd;
};

window.getExtraInformationText = function(database, className, language) {
    let categories = database['categories'];
    let extraInformationText = '';
    let finalClassNameConfig = window.getFinalClassNameConfig(database, className);

    if (finalClassNameConfig === null) {
        return extraInformationText;
    }

    if (finalClassNameConfig['description'][language]) {
        extraInformationText = finalClassNameConfig['description'][language];
    }

    if (finalClassNameConfig['urls']['wikipedia'][language]) {
        extraInformationText += extraInformationText ? '<br /><br />' : '';

        extraInformationText += '<b>Wikipedia:</b> </b>' +
            '<a href="' + finalClassNameConfig['urls']['wikipedia'][language] + '" target="_blank">' +
            finalClassNameConfig['name'][language] +
            '</a>'
        ;
    }

    let categoriesCurrent = finalClassNameConfig['categories'];

    if (categoriesCurrent.length > 0) {
        extraInformationText += '<br />';
    }

    for (let categoryId in categoriesCurrent) {
        let categoryCurrent = categoriesCurrent[categoryId];

        extraInformationText += extraInformationText ? '<br />' : '';
        extraInformationText += '<b>Category:</b> ' +
            '<a href="' + categories[categoryCurrent]['urls']['wikipedia'][language] + '" target="_blank">' +
                categories[categoryCurrent]['name'][language] +
            '</a>'
        ;
    }

    return extraInformationText;
};

window.renewPredictionOverview = function(database, evaluationData, titleTemplate, classTemplate, classTemplateExtraInformation, language) {
    let html = titleTemplate;

    for (let index in evaluationData['prediction_overview_array']) {
        let predictionItem = evaluationData['prediction_overview_array'][index];
        let className = predictionItem['class_name'].replace(/:$/, '');
        let percent = Math.round(predictionItem['predicted_value'] * 100 * 100) / 100;
        let name = window.getName(database, className, language);
        let extraInformationText = window.getExtraInformationText(database, className, language);
        let predictionHtml = '';

        /* add html templates */
        predictionHtml += classTemplate.
            replace(/%\(name\)s/, name).
            replace(/%\(percent\)s/, percent + '%');
        predictionHtml += classTemplateExtraInformation.
            replace(/%\(more\)s/, extraInformationText);

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