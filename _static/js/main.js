function setActiveCurrentStep(id) {
        $('#instructions').removeClass('active');
        $('#training').removeClass('active');
        $('#experiment').removeClass('active');

        if (!$('#' + id).attr('class').includes('active')) {
            $('#' + id).attr('class', 'md-step active');
        }
}