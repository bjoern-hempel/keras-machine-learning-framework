$(document).ready(function() {
    $("#predict-form").submit(function(event) {

        event.preventDefault(); //prevent default action

        let post_url = $(this).attr("action"); //get form action url
        let request_method = $(this).attr("method"); //get form GET/POST method

        let formDataObject = JSON.stringify({
            'number': $(this).find('[name="number"]').val(),
            'language': $(this).find('[name="language"]').val(),
            'output_type': $(this).find('[name="output_type"]').val()
        });
        let formDataJson = JSON.stringify(formDataObject);

        $.ajax({
            url : post_url,
            type: request_method,
            data : formDataJson,
            contentType: 'application/json'
        }).done(function(json) {
            $("#server-results").html(JSON.stringify(json, null, "\t"));
        });
    });
});