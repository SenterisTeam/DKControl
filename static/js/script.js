$(document).ready(function () {
    $('.ui.dropdown').dropdown();

    $("#age-slider").slider({
        max: 18,
        min: 1,
        range: true,
        values: [1, 18],
        slide: function (event, ui) {
            $("#result-age-slider").text("от " + ui.values[0] + " до " + ui.values[1]);
            $('#search-field-age').val(ui.values[0] + "-" + ui.values[1])
        },
    });

    $('.ui.search').search({
        // change search endpoint to a custom endpoint by manipulating apiSettings
        apiSettings: {
            url: '/search/?q={query}&json=true'
        },
        type: 'category',
        minCharacters: 0
    });

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const filters = urlParams.get('filters');
    if (filters) {
        $('.ui.dropdown')
            .dropdown("set selected", filters.split(','));
        $('#search-button').trigger("click")
    }

    $('.select').click(function () {
        $('.select').removeClass('selected');
        $('#select-result').val($(this).attr('value'));
        $(this).addClass('selected')
    });

    $('.attending-checkbox').click(function () {
        let status = "";
        if ($(this).is(":checked")) status = "True";
        $.get(`/attendings/${$(this).attr('name')}/`, {"status": status})
    })

    $('.edit.button').click(function () {
        $('.edit.button').replaceWith($('#save-edit').html())
        let items = $('.basic-info-block .item')
        for (let i = 0; i < items.length; i++) {
            let content = $(items[i]).children('.content.edit')
            let description = content.children('.description')
            if (content.hasClass('string')) {
                let value = description.text()
                if (value === "Не указано") value = "";
                description.html($('#string-edit-input').html());
                description.children().children('input').val(value)
                description.children().children('input').attr('name', content.attr('data-name'))
            } else if (content.hasClass('fio')) {
                let value = description.text()
                description.html($('#fio-edit-input').html());
                description.children().children('input').val(value)
                description.children().children('input').attr('name', 'fio')
            } else if (content.hasClass('date')) {
                let value = description.attr('data-date')
                description.html($('#date-edit-input').html());
                description.children().children('input').val(value)
                description.children().children('input').attr('name', content.attr('data-name'))
            } else if (content.hasClass('select')) {
                let value = description.attr('data-options').split(',')
                let selected = description.text()
                description.html($('#select-edit-input').html());
                for (let i2 in value) {
                    let option = $('<option></option>').val(value[i2]).text(value[i2]);
                    if (value[i2] === selected) option.attr('selected', '')
                    description.children().children('select').append(option)
                }
                description.children().children('select').attr('name', content.attr('data-name'))
            }
        }
    })
});