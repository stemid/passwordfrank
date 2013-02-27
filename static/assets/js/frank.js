$(document).ready(function () {
    'use strict';

    // Setup jquery sliders for random password settings form
    var bitsValue = 12, wordsValue = 5, daysValue = 10, viewsValue = 10,
    url = '', oldSuccessHtml = '', sendData = '';
    $('#bitsSliderValue').html(bitsValue);
    $('#bitsSlider').slider({
        max: 16,
        min: 4,
        value: 12,
        animate: true,
        slide: function (event, ui) {
            bitsValue = ui.value;
            $('#bitsSliderValue').html(bitsValue);
        }
    });

    $('#wordsSliderValue').html(wordsValue);
    $('#wordsSlider').slider({
        max: 10,
        min: 2,
        value: 5,
        animate: true,
        slide: function (event, ui) {
            wordsValue = ui.value;
            $('#wordsSliderValue').html(wordsValue);
        }
    });

    // Fetch random password for input field
    $('#generateRandomPassword1, #generateRandomPassword2').click(function () {
        url = $('#phraseForm').attr('action');
        sendData = {'bits': bitsValue, 'words': wordsValue };

        var jqreq = $.getJSON(url, sendData, function (json) {
            if (json.error) {
                console.log(json.error);
            }
            if (json.phrase) {
                $('#passwordInput').val(json.phrase);
            }
        });
    });

    // Setup sliders for settings form
    $('#daysSliderValue').html(daysValue);
    $('#daysSlider').slider({
        max: 100,
        min: 1,
        value: 10,
        animate: true,
        slide: function (event, ui) {
            daysValue = ui.value;
            $('#daysSliderValue').html(daysValue);
        }
    });

    $('#viewsSliderValue').html(viewsValue);
    $('#viewsSlider').slider({
        max: 100,
        min: 1,
        value: 10,
        animate: true,
        slide: function (event, ui) {
            viewsValue = ui.value;
            $('#viewsSliderValue').html(viewsValue);
        }
    });

    // Post password to API
    $('#phraseForm').submit(function (event) {
        var request;
        var loadingGif = '<img src="/static/assets/img/ajax-loader.gif" alt="Loading..." />';

        // Abort any pending request
        if (request) {
            request.abort();
        }

        // Disable normal submission of form
        event.preventDefault();

        var $form = $(this);
        var $inputs = $form.find('input button');
        var password = $form.find('input[name="phrase"]').val();
        var sendData = {
            'maxdays': daysValue,
            'maxviews': viewsValue,
            'password': password
        };
        url = $form.attr('action');

        // Disable all input controls
        $inputs.prop('disabled', true);

        // Close the alert box, this is stupid UI handling
        $('#postPasswordAlert').alert('close');

        // Fill success alert box with loading gif until request is complete
        oldSuccessHtml = $('#postPasswordSuccess').html();
        $('#postPasswordSuccess').html(loadingGif);

        // Toggle post modal
        $('#postPasswordModal').modal('toggle');

        // Submit the POST query to API
        jqreq = $.ajax({
            type: 'POST',
            url: url,
            cache: false,
            data: sendData,
            dataType: 'json',
            success: function (data, textStatus, jqHXR) {
                $('#postPasswordSuccess').html(oldSuccessHtml);
                $('#passwordLink').val(location.href + data.id);
                $('#passwordLink').focus(function () {
                    $(this).select();
                });
            },
            error: function (jqXHR, textStatus, error) {
                if (error) {
                    $('#postPasswordAlert').append('Failed to post password: ' + textStatus);
                }
                $('#postPasswordAlert').alert();
            },
            complete: function (jqXHR, textStatus) {
            }
        });
    });
});
