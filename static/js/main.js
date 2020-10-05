/** some configs */
window.maxSize = 1024;

/**
 * Class to do some prediction things and shows the content to screen.
 *
 * @author Bjoern Hempel <bjoern@hempel.li>
 * @version 1.0 <2020-10-05>
 */
class PredictionClass {

    /**
     * Some labels.
     *
     * @type {{DE: {accuracy: string, edibility: string}, GB: {accuracy: string, edibility: string}}}
     */
    labels = {
        'DE': {
            'edibility': 'Genie&#223;barkeit',
            'accuracy': 'Genauigkeit'
        },
        'GB': {
            'edibility': 'Edibility',
            'accuracy': 'Accuracy'
        }
    };

    /**
     * Edibility labels.
     *
     * @type {{deadly: {label: {DE: string, GB: string}}, inedible: {label: {DE: string, GB: string}}, psychoactive: {label: {DE: string, GB: string}}, edible: {label: {DE: string, GB: string}}, poisonous: {label: {DE: string, GB: string}}, allergic_reactions: {label: {DE: string, GB: string}}, choice: {label: {DE: string, GB: string}}, inadvisable: {label: {DE: string, GB: string}}}}
     */
    edibilityLabels = {
        'edible': {
            'label': {
                'DE': 'E&#223;bar',
                'GB': 'Edible'
            },
            'class': 'ok',
            'icon': '&#9787;'
        },
        'inedible': {
            'label': {
                'DE': 'Une&#223;bar',
                'GB': 'Inedible'
            },
            'class': 'warn',
            'icon': '&#9888;'
        },
        'poisonous': {
            'label': {
                'DE': 'Giftig',
                'GB': 'Poisonous'
            },
            'class': 'stop',
            'icon': '&#9760;'
        },
        'choice': {
            'label': {
                'DE': 'Erstklassig',
                'GB': 'Choice'
            },
            'class': 'ok',
            'icon': '&#9787;'
        },
        'inadvisable': {
            'label': {
                'DE': 'Nicht zu empfehlen',
                'GB': 'Inadvisable'
            },
            'class': 'warn',
            'icon': '&#9888;'
        },
        'deadly': {
            'label': {
                'DE': 'T&#246;dlich',
                'GB': 'Deadly'
            },
            'class': 'stop',
            'icon': '&#9760;'
        },
        'allergic_reactions': {
            'label': {
                'DE': 'Allergische Reaktionen',
                'GB': 'Allergic Reactions'
            },
            'class': 'warn',
            'icon': '&#9888;'
        },
        'psychoactive': {
            'label': {
                'DE': 'Psychoaktiv',
                'GB': 'Psychoactive'
            },
            'class': 'warn',
            'icon': '&#9888;'
        }
    }

    /**
     * The class constructor.
     *
     * @param maxSize
     */
    constructor(maxSize) {
        this.digits = 2;
        this.maxSize = maxSize;
    }

    /**
     * maxSize getter.
     *
     * @returns {*}
     */
    getMaxSize() {
        return this.maxSize;
    }

    /**
     * Get label.
     *
     * @param name
     * @param language
     * @returns {*}
     */
    getLabel(name, language) {
        return this.labels[language][name];
    }

    /**
     * Returns the edibility labels.
     *
     * @param values
     * @param language
     * @returns {string}
     */
    getEdibility(values, language) {
        let edibility = [];
        let self = this;

        values.forEach(function (item) {
            edibility.push(
                '<span class="%(class)s">%(label)s</span>'.
                    replace('%(class)s', self.edibilityLabels[item]['class']).
                    replace('%(label)s', self.edibilityLabels[item]['label'][language])
            );
        });

        return edibility.join(', ');
    }

    /**
     * Returns the formatted title.
     *
     * @param json
     * @param number
     * @returns {string}
     */
    getTitle(json, number) {
        // Get prediction class
        let predictionClassName = json['data']['prediction_order'][number];
        let predictionClass = json['data']['classes'][predictionClassName];

        let name = predictionClass.name;
        let wikipedia = predictionClass.wikipedia;

        if (wikipedia) {
            name = '<a href="%(link)s" target="_blank">%(name)s</a>'.
                replace('%(link)s', wikipedia).
                replace('%(name)s', name)
        }

        let title =
            '%(number)d) %(name)s'.
            replace('%(number)d', number + 1).
            replace('%(name)s', name);

        return title;
    }

    /**
     * Translate the given json data object to category path.
     *
     * @param json
     * @param number
     * @returns {*}
     */
    getCategoryPath(json, number) {
        // Get prediction class
        let predictionClassName = json['data']['prediction_order'][number];
        let predictionClass = json['data']['classes'][predictionClassName];

        // Translate category path
        let categoryPath = [];

        predictionClass['category_path'].forEach(function (item) {
            let category = json['data']['categories'][item];
            let name = category['name'];
            let wikipedia = category['wikipedia']

            if (wikipedia) {
                categoryPath.push(
                    '<a href="%(link)s" target="_blank">%(name)s</a>'.
                        replace('%(link)s', wikipedia).
                        replace('%(name)s', name)
                );
            } else {
                categoryPath.push(name);
            }
        });

        // Return the category path
        return categoryPath.join(' > ');
    }

    /**
     * Builds one classification content.
     *
     * @param json
     * @param number
     */
    getContent(json, number) {
        // Some configs
        let content = $('div#content');
        let language = json['parameter']['language'];

        // Get data
        let prediction_class_name = json['data']['prediction_order'][number];
        let prediction_class = json['data']['classes'][prediction_class_name];

        // Add class
        content.find('.content > .content-name').html(this.getTitle(json, number));
        content.find('.content > .content-description').text(prediction_class.description);

        // Add category path
        content.find('.content .content-category-path').html(this.getCategoryPath(json, number));

        // Add accuracy
        content.find('.content > .content-accuracy .accuracy-label').html(this.getLabel('accuracy', language));
        content.find('.content > .content-accuracy .accuracy-value').html(
            '%(number)d%'.
            replace(
                '%(number)d',
                Math.round(prediction_class.prediction * 100 * Math.pow(10, this.digits)) / Math.pow(10, this.digits)
            )
        );

        // Add edibility
        content.find('.content > .content-edibility .edibility-label').html(this.getLabel('edibility', language));
        content.find('.content > .content-edibility .edibility-value').html(this.getEdibility(prediction_class['edibility'], language));

        // Add picture
        content.find('.content > .content-image img').attr('src', json['data']['image']['url']).css('display', 'block');

        return content.html();
    }

    /**
     *  Resizes the given file to self.maxSize
     *
     * @param e
     */
    fileChange(e) {
        $('#predict-file-raw').val('');
        $('#predict-file-name').val('');

        let file = e.target.files[0];
        if (file.type != "image/jpeg" && file.type != "image/png") {
            $('#predict-file-source').val('');
            alert('Please only select images in JPG- or PNG-format.');
        }

        let reader = new FileReader();

        reader.onload = function (readerEvent) {
            let image = new Image();
            image.onload = function (imageEvent) {
                let w = image.width;
                let h = image.height;
                let maxSize = prediction.getMaxSize();

                if (w > h) {
                    if (w > maxSize) {
                        h *= maxSize / w;
                        w = maxSize;
                    }
                } else {
                    if (h > maxSize) {
                        w *= maxSize / h;
                        h = maxSize;
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

                $('#predict-file-raw').val(dataUrl);
                $('#predict-file-name').val(file.name);
            };
            image.src = readerEvent.target.result;
        };

        reader.readAsDataURL(file);
    }

    /**
     * Register the ajax uploader.
     */
    register() {
        $("#predict-form").submit(function(event) {
            event.preventDefault(); //prevent default action

            let post_url = $(this).attr("action"); //get form action url
            let request_method = $(this).attr("method"); //get form GET/POST method

            let formDataObject = JSON.stringify({
                'number': $(this).find('[name="number"]').val(),
                'language': $(this).find('[name="language"]').val(),
                'output-type': $(this).find('[name="output-type"]').val(),
                'predict-file-raw': $(this).find('[name="predict-file-raw"]').val(),
                'predict-file-name': $(this).find('[name="predict-file-name"]').val(),
            });
            let formDataJson = JSON.stringify(formDataObject);

            $.ajax({
                url : post_url,
                type: request_method,
                data : formDataJson,
                contentType: 'application/json'
            }).done(function(json) {
                // Disable error, enable success
                $('.error').css('display', 'none');
                $('.success').css('display', 'block');

                // Clear output
                $('div.content-wrapper').html('');

                // Print all predictions
                json['data']['prediction_order'].forEach(function(item, number) {
                    let content = prediction.getContent(json, number);
                    $('div.content-wrapper').html($('div.content-wrapper').html() + content);
                });

                // Add json
                $('#json').attr('class', 'json-success').html(JSON.stringify(json, null, "\t"));
            }).fail(function (jqXHR) {
                let json = jqXHR.responseJSON;

                // Enable error, disable success
                $('.success').css('display', 'none');
                $('.error').css('display', 'block');

                // Add error message
                $('#error-message').css('display', 'block').text(json['message']);

                // Add json
                $('#json').attr('class', 'json-error').html(JSON.stringify(json, null, "\t"));
            });
        });

        let predictFileSource = document.getElementById('predict-file-source');

        if (predictFileSource !== null) {
            predictFileSource.addEventListener('change', prediction.fileChange, false);
        }
    }
}

/* Initialize the PredictionClass */
prediction = new PredictionClass(window.maxSize);

/* Register DOM Ready */
$(document).ready(function() {
    prediction.register();
});