$(document).ready(function () {
    $('#uploadForm').submit(function (event) {
        event.preventDefault();
        uploadImage();
    });

    $('#predictButton').click(function () {
        uploadImage();
    });

    function uploadImage() {
        var file = $('#fileInput')[0].files[0];
        console.log('Selected file:', file);
        if (!file) {
            alert('Please select an image file');
            return;
        }

        var formData = new FormData();
        formData.append('file', file);

        $.ajax({
            url: '/predict',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                console.log('Response:', data);
                // Check if the predicted_class is defined in the response
                if (data.predicted_class !== undefined) {
                    // Update the content of the webpage with the predicted class
                    $('#prediction').text('Predicted class: ' + data.predicted_class);
                } else {
                    // Handle the case when the predicted_class is undefined
                    $('#prediction').text('Prediction not available');
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                alert('An error occurred during prediction');
            }
        });
    }
});
