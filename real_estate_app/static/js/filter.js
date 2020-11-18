
const all_data = {

}

document.onclick = function (e) {
    if (e.target.classList.contains('checked-inputs')) {
        
        var checked_types= new Array()
        var checked_statuses=new Array()
        document.querySelectorAll('.checked-inputs').forEach(function (e) {
            if (e.classList.contains('types')) {
                if (e.checked == true) {
                    var checked_type = e.closest('.ally').querySelector('.choose-types').innerText
                    checked_types.push(checked_type)
                    
                }
            }
            if (e.classList.contains('feature') && e.checked == true) {
                var checked_status = e.closest('.ally').querySelector('.choose-types').innerText
                checked_statuses.push(checked_status)
            }

        })
        all_data['checked_types'] = checked_types
        all_data['checked_statuses'] = checked_statuses
        loadAllData(all_data)

    }
}

document.querySelector('.select-items').addEventListener('click',(e)=>{
    var selected_city=document.querySelector('.select-selected').innerText
    all_data['selected_city'] = selected_city
    loadAllData(all_data)
})


document.querySelector('.min-price').addEventListener('input', (e) => {
    var minPrice = document.querySelector('.min-price').value
    all_data['minPrice'] = minPrice
    loadAllData(all_data)
})
document.querySelector('.max-price').addEventListener('input', (e) => {
    var maxPrice = document.querySelector('.max-price').value
    all_data['maxPrice'] = maxPrice
    loadAllData(all_data)
})

function loadAllData(data) {
    $.ajax({
        url: 'http://127.0.0.1:5000/getproduct',
        method: "GET",
        data: data,
        success: function (response) {
            document.querySelector('.removed-data').innerHTML = ''
            for (product of response.products) {
                document.querySelector('.removed-data').innerHTML +=`
                <div class="col-4 pb-3">
                <div class="card" style="width: 18rem;">
                    <img src="${ product.image }" class="card-img-top" style="height: 250px;" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">${product.title}</h5>
                        <div class="d-flex justify-content-between">
                            <p>${product.city.title}</p>
                            <span>${product.price}</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <p class="card-text pb-2">${product.short_description}</p>
                            <span>${product.created_at}</span>
                        </div>

                        <a href="/detail/${product.id}"
                            class="btn btn-secondary w-100 detail-button rounded-0">Detail page</a>
                    </div>
                </div>
            </div>`
                
            }
            document.querySelector('.old-pagi').innerHTML=''
            document.querySelector('.js-pagination').innerHTML=''
            for (var i =1;i<=response.page_range;i++){
                page_numbers=document.createElement('span')
                page_numbers.innerText=i
                page_numbers.href=`?page=${i}`
                document.querySelector('.js-pagination').appendChild(page_numbers)
                page_numbers.classList.add('m-2','pagination-numbers-js')

                page_numbers.addEventListener('click',function(){
                    all_data['page']=this.innerText
                    loadAllData(all_data)
                })
            }
            
        },
        error: function (error) {
            console.log(error)
        }
    })
}