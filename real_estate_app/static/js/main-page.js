document.getElementById('search').addEventListener('input', function () {
    
    var searchInput = document.getElementById('search');
    var inputValue = searchInput.value;
    // console.log(inputValue);
    $.ajax({
        url: 'http://127.0.0.1:5001/search',
        method: 'GET',
        data: {
            'inputValue': inputValue,
        },
        success: function (response) {
            console.log(response);
            $('.empty').html('')
            let formDiv = $(`<div class="form-div w-100"><div>`);
            $('.empty').append(formDiv)
            if (inputValue) {
                for (let object of response.products) {

                    $('.form-div').append(`<a class="w-100 mt-1 mb-1" href="/detail/${object.id}"> <span class="ml-3 added-span">${object.title}</span></a>`)

                }
            }
        },
        error: function (error_response) {
            console.log(error_response);
        }
    })
});


