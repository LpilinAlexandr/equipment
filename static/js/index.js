$(function(){
    $("#add").click(function () {
        $.ajax({
            type: "GET",
            url: "ajax_form/",
            data: {
                'typeEquip': $("#selectType").val(),
                'textContent': $("#textContent").val()
            },
            dataType: "text",
            cache: false,
            success: function (data) {
                // Если тип оборудования не был выбран
                if (data == 'missingTypeEquip') {
                    alert('Выберите тип оборудования!');
                }
                // Если не было совпадений по данному типу оборудования
                else if (data == 'NO') {
                    $("#catImg").show().delay(2500).fadeOut();
                }
                // Если были совпадения
                else{
                    $('#haroldTitle').text(data);
                    $("#haroldImg").show().delay(2500).fadeOut();
                }
            }
        });
    });
});
