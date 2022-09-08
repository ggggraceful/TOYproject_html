$(document).ready(function () {
    listing();
});

function listing() {
    $.ajax({
        type: 'GET',
        url: '/write',
        data: {},
        success: function (response) {
            let rows = response['writes']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let image = rows[i]['image']
                let heart = rows[i]['heart']
                let result = rows[i]['result']
                let id = rows[i]['id']
                let text = rows[i]['text']

                let heart_image = '❤'

                let temp_html = `<div class="col">
                         <div class="card">
                         <h5 class="card-title"><b>${title}</b></h5>
                         <img src="${image}"
                             class="card-img-top" alt="빈 이미지" width="470px" height="590px">
                         <div class="card-body">
                            <input type='button'
                                   class="card_btn_heart"
                                   onclick='count("plus")'
                                   value='${heart_image}️'/>
                            <div id='heart_result'>0</div>
                             <p>${heart}</p>
                             <p><b>${id}</b>${text}</p>
                         </div>
                     </div>
                 </div>`;
                $('#cards-box').append(temp_html)

            }
        }
    })
}

function posting() {
    let title = $('#title').val()
    let image = $('#image').val()
    let heart = $('#heart').val()
    let id = $('#id').val()
    let text = $('#text').val()

    $.ajax({
        type: 'POST',
        url: '/write',
        data: {title_give: title, image_give: image, heart_give: heart, id_give: id, text_give: text,},
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    });
}

// window.onload = function () {
//   var btn_write = document.getElementById("nav_btn_write");
//
//   btn_write.onclick = function () {
//     let content = `<div class="col">
//                 <div class="card">
//                     <h5 class="card-title"><b>아이디</b></h5>
//                     <img src="https://movie-phinf.pstatic.net/20220720_283/1658284839003UzxoT_JPEG/movie_image.jpg"
//                         class="card-img-top" alt="빈 이미지" width="470px" height="590px">
//                     <div class="card-body">
//                         <button class="card_btn_heart">
//                             <p onmouseover="this.innerText='❤️'" onmouseout="this.innerText='🤍'">🤍</p>
//                         </button>
//                         <p>좋아요 0개</p>
//                         <p class="card-text">내용</p>
//                     </div>
//                 </div>
//             </div>`;
//
//     $(".list_add").append(content);
//   };
// };
