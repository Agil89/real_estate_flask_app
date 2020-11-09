
const all_data = {

}


document.onclick = function (e) {
    if (e.target.classList.contains('checked-inputs')) {
        
        var checked_types= new Array()
        var checked_status=new Array()
        document.querySelectorAll('.checked-inputs').forEach(function (e) {
            if (e.classList.contains('types')) {
                if (e.checked == true) {
                    var checked_type = e.closest('.ally').querySelector('.choose-types').innerText
                    checked_types.push(checked_type)
                    console.log(checked_type)
                    
                }
            }
            if (e.classList.contains('feature') && e.checked == true) {
                var checked_status = e.closest('.ally').querySelector('.choose-types').innerText
                console.log(checked_status)
                checked_status.push(checked_status)
            }

        })
        all_data['checked_types'] = checked_types
        all_data['checked_status'] = checked_status
        loadAllData(all_data)

    }
}







// document.onclick = function (e) {
//     if (e.target.classList.contains('checked-inputs')) {
        
//         var status_types= new Array()
//         var estate_types=new Array()
//         document.querySelectorAll('.checked-inputs').forEach(function (e) {
//             if (e.classList.contains('types')) {
//                 if (e.checked == true) {
//                     var estate_type = e.closest('.d-flex').querySelector('.choose-types').innerText
//                     estate_types.push(estate_type)
                    
//                 }
//             }
//             if (e.classList.contains('feature') && e.checked == true) {
//                 var status_type = e.closest('.d-flex').querySelector('.choose-types').innerText
//                 status_types.push(status_type)
//             }

//         })
//         all_data['estate_types'] = estate_types
//         all_data['status_types'] = status_types
//         loadAllData(all_data)

//     }
// }


// document.onclick = function(e){
//     if (e.target.classlist.contains('container')){
//         document.querySelectorAll('.')
//     }
// }

// document.querySelectorAll('.container').forEach(function(item){
//     item.addEventListener('click',function(){
//         console.log('hello my love')
//         console.log('byebye')
//     })


// })

// document.querySelector('.select-selected').addEventListener('click',(e)=>{
//     var selected_city=document.querySelector('.select-selected').innerText
//     console.log(selected_city)
//     all_data['selected_city'] = selected_city
//     loadAllData(all_data)
// })



// document.querySelectorAll('.checkmark').forEach(addEventListener('click',(e)=>{
//     console.log('gello')
//     var ele = document.getElementsByName('radioo'); 
//     for(i = 0; i < ele.length; i++) { 
//         if(ele[i].checked) 
//             var selected_type=ele[i].innerText
//     } 
//     console.log(selected_type)
//     all_data['selected_type'] = selected_type
//     loadAllData(all_data)
// }))




// document.querySelector('.min-price').addEventListener('input', (e) => {
//     var minPrice = document.querySelector('.min-price').value
//     all_data['minPrice'] = minPrice
//     loadAllData(all_data)
// })
// document.querySelector('.max-price').addEventListener('input', (e) => {
//     var maxPrice = document.querySelector('.max-price').value
//     all_data['maxPrice'] = maxPrice
//     loadAllData(all_data)
// })

// function loadAllData(data) {
//     console.log(data)
//     $.ajax({
//         url: 'http://127.0.0.1:5001/getproduct',
//         method: "GET",
//         data: data,
//         success: function (response) {
//             console.log(response)
//             document.querySelector('.removed-data').innerHTML = ''
//             console.log(response.page_range)
//             for (cake of response.filtered_cakes) {
//                 document.querySelector('.removed-data').innerHTML +=`
//                 <div class="col-4 parent-of-card">
//                         <div class="card">
//                             <img src="${cake.main_image}" class="card-img-top" alt="...">
//                             <div class="card-body">
//                                 <h5 class="card-title">${cake.name}</h5>
//                                 <div class="d-flex justify-content-between w-100">
//                                     <div>
//                                         <span style="font-size: 14px;">Мин. заказ</span>
//                                     </div>
//                                     <div>
//                                         <span style="font-size: 14px;">${cake.unit}</span>
//                                         <span style="font-size: 14px;">${cake.name_of_unit}</span>
//                                     </div>
//                                 </div>
//                                 <div class="d-flex justify-content-between w-100">
//                                     <div>
//                                         <span style="font-size: 14px;">Стоимость <small class="text-muted">(за мин. заказ)</small></span>
//                                     </div>
//                                     <div>
//                                         <span>${cake.price}</span>

//                                     </div>
//                                 </div>
//                                 <div class="py-2 mt-2">
//                                     <a href="${cake.my_url}"
//                                     class="btn btn-primary w-100 ">Открыть</a>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>`
                
//             }
//             document.querySelector('.old-pagi').innerHTML=''
//             document.querySelector('.js-pagination').innerHTML=''
//             for (var i =1;i<=response.page_range;i++){
//                 page_numbers=document.createElement('span')
//                 page_numbers.innerText=i
//                 page_numbers.href=`?page=${i}`
//                 document.querySelector('.js-pagination').appendChild(page_numbers)
//                 page_numbers.classList.add('m-2','pagination-numbers-js')

//                 page_numbers.addEventListener('click',function(){
//                     all_data['page']=this.innerText
//                     loadAllData(all_data)
//                 })
//             }
            
//         },
//         error: function (error) {
//             console.log(error)
//         }
//     })
// }