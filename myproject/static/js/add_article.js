
function getCookie(name){    //쿠키에서 csrftoken 불러온다
    var cookieValue=null;
    if(document.cookie && document.cookie !==''){
       var cookies=document.cookie.split(';');
       for(var i =0 ; i< cookies.length; i++){
         var cookie=cookies[i].trim();
         if(cookie.substring(0, name.length+1)===(name+'=')){
              var my_token=cookie.substring(name.length+1);
              cookieValue=decodeURIComponent(my_token);
              break;
         }
       }
    }    
    return cookieValue;
 }

document.addEventListener("DOMContentLoaded", function() {
    var element = document.querySelector(".create_article");
    element.addEventListener("click", function() {
        const modalOverlay = document.createElement('div');         // 모달오버레이 div 생성
        const modal_box = document.createElement('div');            // 모달         div 생성
        const modalContent = document.createElement('div');         // 모달 콘텐트   div 생성
        const modalCloseButton = document.createElement('button');  // 모달클로즈    
    
        modalOverlay.classList.add('modal-overlay'); // 모달오버레이 div에 class 속성 추가
        modal_box.classList.add('modal');           // 모달 박스 div에 class 속성 추가
        modalContent.classList.add('modal-content','drop_area', 'drop'); // 모달콘텐트 div에 class 속성 추가
        modalCloseButton.classList.add('modal-close'); // 모달 button class 속성 추가
        modalCloseButton.innerHTML = '&times;'; // 모달 닫기 아이콘 추가
    
        document.body.appendChild(modalOverlay);
        modalOverlay.appendChild(modal_box);
        modal_box.appendChild(modalCloseButton);
        modal_box.appendChild(modalContent);
        modalOverlay.style.display = 'block';
        modalContent.style.display = 'block';
        modalContent.style.justifyContent = 'center';


        modalOverlay.addEventListener("click", function() {
            modalOverlay.style.display = 'none';
        });
        modal_box.addEventListener('click', function(event) {
            event.stopPropagation();
        });
        modalCloseButton.addEventListener('click', function(event) {
            modalOverlay.style.display = 'none';
        });
        // 여기까지가 기본 모달 생성

        const title_div=document.createElement('div'); 
        title_div.classList.add('add_article_modal_title_div'); 
        title_div.innerHTML="새 게시물 만들기";
        modalContent.appendChild(title_div);

        const add_box_div=document.createElement('div'); 
        add_box_div.classList.add('add_box_div'); 
        modalContent.appendChild(add_box_div);
        const svg_text_button_div=document.createElement('div'); 
        add_box_div.appendChild(svg_text_button_div);

        const svg_div=document.createElement('div'); 
        svg_div.classList.add('svg_div'); 

        const text_div=document.createElement('div'); 
        text_div.classList.add('text_div'); 

        //const button_div=document.createElement('div'); 
        svg_text_button_div.appendChild(svg_div);
        svg_text_button_div.appendChild(text_div);
        //svg_text_button_div.appendChild(button_div);


        const svgCode = `
        <svg aria-label="이미지나 동영상과 같은 미디어를 나타내는 아이콘" 
            class="x1lliihq x1n2onr6" 
            color="rgb(0, 0, 0)" 
            fill="rgb(0, 0, 0)" 
            height="77" 
            role="img" 
            viewBox="0 0 97.6 77.3" 
            width="96">
                <title>이미지나 동영상과 같은 미디어를 나타내는 아이콘</title>
                <path d="M16.3 24h.3c2.8-.2 4.9-2.6 4.8-5.4-.2-2.8-2.6-4.9-5.4-4.8s-4.9 2.6-4.8 5.4c.1 2.7 2.4 4.8 5.1 4.8zm-2.4-7.2c.5-.6 1.3-1 2.1-1h.2c1.7 0 3.1 1.4 3.1 3.1 0 1.7-1.4 3.1-3.1 3.1-1.7 0-3.1-1.4-3.1-3.1 0-.8.3-1.5.8-2.1z" 
                fill="currentColor">
                </path>
                <path d="M84.7 18.4 58 16.9l-.2-3c-.3-5.7-5.2-10.1-11-9.8L12.9 6c-5.7.3-10.1 5.3-9.8 11L5 51v.8c.7 5.2 5.1 9.1 10.3 9.1h.6l21.7-1.2v.6c-.3 5.7 4 10.7 9.8 11l34 2h.6c5.5 0 10.1-4.3 10.4-9.8l2-34c.4-5.8-4-10.7-9.7-11.1zM7.2 10.8C8.7 9.1 10.8 8.1 13 8l34-1.9c4.6-.3 8.6 3.3 8.9 7.9l.2 2.8-5.3-.3c-5.7-.3-10.7 4-11 9.8l-.6 9.5-9.5 10.7c-.2.3-.6.4-1 .5-.4 0-.7-.1-1-.4l-7.8-7c-1.4-1.3-3.5-1.1-4.8.3L7 49 5.2 17c-.2-2.3.6-4.5 2-6.2zm8.7 48c-4.3.2-8.1-2.8-8.8-7.1l9.4-10.5c.2-.3.6-.4 1-.5.4 0 .7.1 1 .4l7.8 7c.7.6 1.6.9 2.5.9.9 0 1.7-.5 2.3-1.1l7.8-8.8-1.1 18.6-21.9 1.1zm76.5-29.5-2 34c-.3 4.6-4.3 8.2-8.9 7.9l-34-2c-4.6-.3-8.2-4.3-7.9-8.9l2-34c.3-4.4 3.9-7.9 8.4-7.9h.5l34 2c4.7.3 8.2 4.3 7.9 8.9z" 
                fill="currentColor">
                </path>
                <path d="M78.2 41.6 61.3 30.5c-2.1-1.4-4.9-.8-6.2 1.3-.4.7-.7 1.4-.7 2.2l-1.2 20.1c-.1 2.5 1.7 4.6 4.2 4.8h.3c.7 0 1.4-.2 2-.5l18-9c2.2-1.1 3.1-3.8 2-6-.4-.7-.9-1.3-1.5-1.8zm-1.4 6-18 9c-.4.2-.8.3-1.3.3-.4 0-.9-.2-1.2-.4-.7-.5-1.2-1.3-1.1-2.2l1.2-20.1c.1-.9.6-1.7 1.4-2.1.8-.4 1.7-.3 2.5.1L77 43.3c1.2.8 1.5 2.3.7 3.4-.2.4-.5.7-.9.9z" 
                fill="currentColor">
                </path>
        </svg>`;
        svg_div.innerHTML=svgCode;
        text_div.innerHTML='사진과 동영상을 여기에 끌어다 놓으세요';
        

        //const insert_file_button = document.createElement('button');         // 모달오버레이 div 생성
        //insert_file_button.textContent="컴퓨터에서 선택";
        //add_box_div.appendChild(insert_file_button);

        const imageInput = document.createElement('input');
        imageInput.type = 'file';
        imageInput.id = 'imageInput';
        imageInput.accept = 'image/*'; // accept 속성 설정
        //imageInput.multiple = true; // multiple 속성 설정 (다중 파일 선택 허용)

        add_box_div.appendChild(imageInput);

        const preview_div=document.createElement('div');
        preview_div.classList.add('preview_div'); // 모달 button class 속성 추가

        const preview_img=document.createElement('img');
        preview_img.style.width = '10%';

        preview_img.classList.add('preview_img'); // 모달 button class 속성 추가

        preview_div.appendChild(preview_img);
        svg_text_button_div.appendChild(preview_div);
        svg_text_button_div.classList.add('svg_text_button_div'); // 모달 button class 속성 추가

        //본문 입력하는 textarea
        const textarea = document.createElement("textarea");
        svg_text_button_div.appendChild(textarea);

        // '업로드' 버튼 생성

        const upload_button=document.createElement("button");
        upload_button.classList.add('upload_button'); // 모달 button class 속성 추가
        upload_button.innerHTML = "<b>Upload</b>"; // 버튼의 HTML 내용을 변경
        svg_text_button_div.appendChild(upload_button);
        

        // 버튼으로 이미지 추가
        imageInput.addEventListener('change', () => {
            console.log("imageinput change");
            const file = imageInput.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    preview_img.src = event.target.result;
                    preview_div.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
        modalContent.addEventListener('dragover', (e) => {
            e.preventDefault();
            add_box_div.style.border = '2px dashed red';
        });        
        modalContent.addEventListener('dragleave', (e) => {
            e.preventDefault();
            add_box_div.style.border = 'none';
        });        
        modalContent.addEventListener('drop', (e) => {
            e.preventDefault();
            add_box_div.style.border = 'none';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                // 파일을 input에 추가
                console.log(files);
                const newFile = new File([files[0]], files[0].name, { type: files[0].type });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(newFile);
                imageInput.files = dataTransfer.files;
            }
        });

        upload_button.addEventListener("click", function() {
            console.log("run crate_article ajax");
            const csrftoken=getCookie('csrftoken');
            const urlNode = document.getElementById('createArticleUrl');
            const url_value = urlNode.getAttribute('create_article_url');

            console.log("url : "+url_value);
            const file = imageInput.files[0];

            const fileExtension = file.name.split('.').pop().toLowerCase();
            const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'jfif'];
            const videoExtensions = ['mp4', 'avi', 'mkv', 'mov'];
            const formData = new FormData();
            if (imageExtensions.includes(fileExtension)) {
                console.log("이미지다!");
                formData.append('image', file);
                formData.append('type', 'image');
                formData.append('content_type', '1');

            } else if (videoExtensions.includes(fileExtension)) {
                console.log("비디오다!");
                formData.append('video', file);
                formData.append('type', 'video');
                formData.append('content_type', '2');

            } else {
                alert('이 파일은 이미지나 비디오가 아닙니다.');
                return;
            }
            formData.append('content', textarea.value);
            console.log(formData);
            $.ajax({
                type: 'POST',
                url: url_value,
                headers: {"X-CSRFToken":csrftoken},
                data: formData,
                processData: false,
                contentType: false,                
                success: function (response) {
//                    console.log("success : "+response.message);
//                    modalCloseButton.click();
                    modalOverlay.style.display = 'none';
                }
            });
        });
    });
});
