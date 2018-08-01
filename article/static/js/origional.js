function overShow(obj,e) {
    var showDiv = document.getElementById('showDiv');
    var theEvent = window.event|| e;
    var scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
    var scrollY = document.documentElement.scrollTop || document.body.scrollTop;
    var x = e.pageX || e.clientX + scrollX;
    var y = e.pageY || e.clientY + scrollY;
    showDiv.style.left = x+'px';
    showDiv.style.top = y+'px';
    showDiv.style.display = 'block';
    //alert(obj.innerHTML);
    showDiv.innerHTML = obj.innerHTML;
}

function outHide() {
    var showDiv = document.getElementById('showDiv');
    showDiv.style.display = 'none';
    showDiv.innerHTML = '';
}


function imgRefresh1() {
    document.getElementById('imgshow').setAttribute("src","img/boy_glasses.jpg");
}
function imgRefresh2() {
    document.getElementById('imgshow').setAttribute("src","img/boy_sport.jpg");
}
function imgRefresh3() {
    document.getElementById('imgshow').setAttribute("src","img/boy_hat.jpg");
}
function imgRefresh4() {
    document.getElementById('imgshow').setAttribute("src","img/girl_rollhair.jpg");
}
function imgRefresh5() {
    document.getElementById('imgshow').setAttribute("src","img/girl_shorthair.jpg");
}
function imgRefresh6() {
    document.getElementById('imgshow').setAttribute("src","img/girl_silent.jpg");
}

function nowFitShow() {
    document.getElementById('imgnow').setAttribute("src",document.getElementById('imgshow').src);
}

function showFitNow() {
    document.getElementById('imgshow').setAttribute("src",document.getElementById('imgnow').src);
}

$('#boyg').on('click', imgRefresh1);
$('#boys').on('click', imgRefresh2);
$('#boyh').on('click', imgRefresh3);
$('#girlr').on('click', imgRefresh4);
$('#girlsh').on('click', imgRefresh5);
$('#girlsi').on('click', imgRefresh6);
$('#imgsave').on('click', nowFitShow);
$('#changeimg').on('click', showFitNow);



function loadData()
{
    var xmlhttp;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET","x_mailbox_demo.html",false);
    xmlhttp.send();
    document.getElementById("update").innerHTML=xmlhttp.responseText;
}




function firstactive2() {
    var Friends = {};
    for(i=1; document.getElementById("friend"+i) !== null; i++){
        Friends[i] = document.getElementById("friend"+i);
    }
    var Friendlist = document.getElementById("friendlist");
        if(Friends && Friendlist.classList.contains("active")) {
            Friends[1].classList.remove("info-element");
            Friends[1].classList.add("white-element");
            for(i=2;document.getElementById("friend"+i) !== null;i++){
                Friends[i].classList.remove("white-element");
                Friends[i].classList.add("info-element");
            }

        }
}

function firstactive() {
    var Friend1 = document.getElementById("friend1");
    var Friend2 = document.getElementById("friend2");
    var Friend3 = document.getElementById("friend3");
    var Friend4 = document.getElementById("friend4");
    var Friend5 = document.getElementById("friend5");
    var Friend6 = document.getElementById("friend6");
    var roomnamelist = xxx;

    if(Friendlist.classList.contains("active")) {
        Friend1.classList.remove("info-element");
        Friend1.classList.add("white-element");
        if (roomnamelist != "") {
            Friend2.classList.remove("white-element");
            Friend2.classList.remove("info-element");
            Friend2.classList.add("danger-element");
        }
        else {
            Friend2.classList.remove("white-element");
            Friend2.classList.remove("danger-element");
            Friend2.classList.add("info-element");
        }

        if (roomnamelist != "") {
            Friend3.classList.remove("white-element");
            Friend3.classList.remove("info-element");
            Friend3.classList.add("danger-element");
        }
        else {
            Friend3.classList.remove("white-element");
            Friend3.classList.remove("danger-element");
            Friend3.classList.add("info-element");
        }

        if (roomnamelist != "") {
            Friend4.classList.remove("white-element");
            Friend4.classList.remove("info-element");
            Friend4.classList.add("danger-element");
        }
        else {
            Friend4.classList.remove("white-element");
            Friend4.classList.remove("danger-element");
            Friend4.classList.add("info-element");
        }

        if (roomnamelist != "") {
            Friend5.classList.remove("white-element");
            Friend5.classList.remove("info-element");
            Friend5.classList.add("danger-element");
        }
        else {
            Friend5.classList.remove("white-element");
            Friend5.classList.remove("danger-element");
            Friend5.classList.add("info-element");
        }

        if (roomnamelist != "") {
            Friend6.classList.remove("white-element");
            Friend6.classList.remove("info-element");
            Friend6.classList.add("danger-element");
        }
        else {
            Friend6.classList.remove("white-element");
            Friend6.classList.remove("danger-element");
            Friend6.classList.add("info-element");
        }
    }
}

function talk() {
    var Words = document.getElementById("chatshow");
    var TalkWords = document.getElementById("chatinput");
    var TalkSub = document.getElementById("talksub");
    var date = new Date();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var currentTime =  hour + ":" + minute;
        //定义空字符串
        var str = "";
        if(TalkWords.value == ""){
            return;
        }
        str =   '<div class="right">' +
                '<div class="author-name">' +
                '<a href="x_personal_page_show_demo.html" target="_blank" style="color: #0d8ddb"><strong>我</strong></a>' +
                '<small class="chat-date">' +
                 currentTime +
                '</small>' +
                '</div>' +
                '<div class="chat-message">' +
                 TalkWords.value +
                '</div>' +
                '</div>'
                +'<br>';
        Words.innerHTML = Words.innerHTML + str;
        Words.scrollTop = Words.scrollHeight;
    TalkWords.value = "";
}

function Recieve() {
    var Words = document.getElementById("chatshow");
    var str = "";
    var str2 = str;

    function getJson()
    {
        $.getJSON("js/userinfo.json", function (data) {
            $.each(data, function (infoIndex, info) {
                str =   '<div class="left">' +
                        '<div class="author-name">' +
                        '<a href="x_personal_page_show_demo.html" target="_blank" style="color: #0d8ddb"><strong>info["name"]</strong></a>' +
                        '<small class="chat-date">' +
                        'info["time"]' +
                        '</small>' +
                        '</div>' +
                        '<div class="chat-message active">' +
                        'info["message"]' +
                        '</div>' +
                        '</div>' +
                        '<br>';
            });
        });
    }

    if(str2 === str){
        setTimeout("getJson()",1000);
    }
    else {
        str2 = str;
    }

    if (str != "") {
        Words.innerHTML = Words.innerHTML + str;
        Words.scrollTop = Words.scrollHeight;
    }
    setTimeout("Recieve()",1000);
}

function Getid(event) {
    var Fiid = event.target;
    var i = event.target.id;
    if(event.target.tagName.toUpperCase() !== "LI") {
        i = event.target.parentNode.id;
    }
    return i;
}

function Justice() {
    var Friends = {};
    var colors = {};
    var friendid = Getid(event);
    for(i=1; document.getElementById("friend"+i) !== null; i++){
        Friends[i] = document.getElementById("friend"+i);
        colors[i] = Friends[i].classList.contains("info-element")
        if(Friends[i].id === friendid){
            if (colors[i] == true) {
                Friends[i].classList.remove("info-element");
                Friends[i].classList.add("white-element");
            }
            else {
                Friends[i].classList.remove("danger-element");
                Friends[i].classList.add("white-element");
            }
        }
    }


    // var Friend1 = document.getElementById("friend1");
    // var Friend2 = document.getElementById("friend2");
    // var Friend3 = document.getElementById("friend3");
    // var Friend4 = document.getElementById("friend4");
    // var Friend5 = document.getElementById("friend5");
    // var Friend6 = document.getElementById("friend6");
    // var color1 = Friend1.classList.contains("info-element");
    // var color2 = Friend2.classList.contains("info-element");
    // var color3 = Friend3.classList.contains("info-element");
    // var color4 = Friend4.classList.contains("info-element");
    // var color5 = Friend5.classList.contains("info-element");
    // var color6 = Friend6.classList.contains("info-element");

    // if (friendid === "friend1") {
    //
    //
    // }
    //
    // if (friendid === "friend2") {
    //     if (color2 == true) {
    //         Friend2.classList.remove("info-element");
    //         Friend2.classList.add("white-element");
    //     }
    //     else {
    //         Friend2.classList.remove("danger-element");
    //         Friend2.classList.add("white-element");
    //     }
    // }
    //
    // if (friendid === "friend3") {
    //     if (color3 == true) {
    //         Friend3.classList.remove("info-element");
    //         Friend3.classList.add("white-element");
    //     }
    //     else {
    //         Friend3.classList.remove("danger-element");
    //         Friend3.classList.add("white-element");
    //     }
    // }
    //
    // if(friendid === "friend4") {
    //     if (color4 == true) {
    //         Friend4.classList.remove("info-element");
    //         Friend4.classList.add("white-element");
    //     }
    //     else {
    //         Friend4.classList.remove("danger-element");
    //         Friend4.classList.add("white-element");
    //     }
    // }
    //
    // if (friendid === "friend5") {
    //     if (color5 == true) {
    //         Friend5.classList.remove("info-element");
    //         Friend5.classList.add("white-element");
    //     }
    //     else {
    //         Friend5.classList.remove("danger-element");
    //         Friend5.classList.add("white-element");
    //     }
    // }
    //
    // if (friendid === "friend6") {
    //     if (color6 == true) {
    //         Friend6.classList.remove("info-element");
    //         Friend6.classList.add("white-element");
    //     }
    //     else {
    //         Friend6.classList.remove("danger-element");
    //         Friend6.classList.add("white-element");
    //     }
    // }
}

function Alljustice() {
    var Friends = {};
    var colors = {};
    for(i=1; document.getElementById("friend"+i) !== null; i++){
        Friends[i] = document.getElementById("friend"+i);
        colors[i] = Friends[i].classList.contains("white-element")
    }
    i -= 1;
    // alert("i="+i);
    for(m=1; m<=i; m++){
        if(colors[m] == true){
            for(j=1;j<=i;j++){
                if(j !== m && colors[j] == true){
                    Friends[j].classList.remove("white-element");
                    Friends[j].classList.add("info-element");
                }
            }
        }
    }





    // var Friend1 = document.getElementById("friend1");
    // var Friend2 = document.getElementById("friend2");
    // var Friend3 = document.getElementById("friend3");
    // var Friend4 = document.getElementById("friend4");
    // var Friend5 = document.getElementById("friend5");
    // var Friend6 = document.getElementById("friend6");
    // var color1 = Friend1.classList.contains("white-element");
    // var color2 = Friend2.classList.contains("white-element");
    // var color3 = Friend3.classList.contains("white-element");
    // var color4 = Friend4.classList.contains("white-element");
    // var color5 = Friend5.classList.contains("white-element");
    // var color6 = Friend6.classList.contains("white-element");
    // if(color1 == true){
    //     if(color2 == true){
    //         Friend2.classList.remove("white-element");
    //         Friend2.classList.add("info-element");
    //     }
    //     if(color3 == true){
    //         Friend3.classList.remove("white-element");
    //         Friend3.classList.add("info-element");
    //     }
    //     if(color4 == true){
    //         Friend4.classList.remove("white-element");
    //         Friend4.classList.add("info-element");
    //     }
    //     if(color5 == true){
    //         Friend5.classList.remove("white-element");
    //         Friend5.classList.add("info-element");
    //     }
    //     if(color6 == true){
    //         Friend6.classList.remove("white-element");
    //         Friend6.classList.add("info-element");
    //     }room_name
    // }
    // if(color2 == true){
    //     if(color1 == true){
    //         Friend1.classList.remove("white-element");
    //         Friend1.classList.add("info-element");
    //     }
    //     if(color3 == true){
    //         Friend3.classList.remove("white-element");
    //         Friend3.classList.add("info-element");
    //     }id="zhmsgtest"
    //     if(color4 == true){
    //         Friend4.classList.remove("white-element");
    //         Friend4.classList.add("info-element");
    //     }
    //     if(color5 == true){
    //         Friend5.classList.remove("white-element");
    //         Friend5.classList.add("info-element");
    //     }
    //     if(color6 == true){
    //         Friend6.classList.remove("white-element");
    //         Friend6.classList.add("info-element");
    //     }
    // }
    // if(color3 == true){
    //     if(color1 == true){id="zhmsgtest"
    //         Friend1.classList.remove("white-element");
    //         Friend1.classList.add("info-element");
    //     }
    //     if(color2 == true){
    //         Friend2.classList.remove("white-element");
    //         Friend2.classList.add("info-element");
    //     }
    //     if(color4 == true){
    //         Friend4.classList.remove("white-element");
    //         Friend4.classList.add("info-element");
    //     }
    //     if(color5 == true){
    //         Friend5.classList.remove("white-element");
    //         Friend5.classList.add("info-element");
    //     }
    //     if(color6 == true){
    //         Friend6.classList.remove("white-element");
    //         Friend6.classList.add("info-element");
    //     }room_name
    // }
    // if(color4 == true){
    //     if(color1 == true){
    //         Friend1.classList.remove("white-element");
    //         Friend1.classList.add("info-element");
    //     }
    //     if(color2 == true){
    //         Friend2.classList.remove("white-element");
    //         Friend2.classList.add("info-element");
    //     }
    //     if(color3 == true){
    //         Friend3.classList.remove("white-element");
    //         Friend3.classList.add("info-element");
    //     }
    //     if(color5 == true){
    //         Friend5.classList.remove("white-element");
    //         Friend5.classList.add("info-element");
    //     }
    //     if(color6 == true){
    //         Friend6.classList.remove("white-element");
    //         Friend6.classList.add("info-element");
    //     }
    // }
    // if(color5 == true){
    //     if(color1 == true){
    //         Friend1.classList.remove("white-element");
    //         Friend1.classList.add("info-element");
    //     }
    //     if(color2 == true){
    //         Friend2.classList.remove("white-element");
    //         Friend2.classList.add("info-element");
    //     }
    //     if(color3 == true){
    //         Friend3.classList.remove("white-element");
    //         Friend3.classList.add("info-element");
    //     }
    //     if(color4 == true){
    //         Friend4.classList.remove("white-element");
    //         Friend4.classList.add("info-element");
    //     }
    //     if(color6 == true){
    //         Friend6.classList.remove("white-element");
    //         Friend6.classList.add("info-element");
    //     }
    // }
    // if(color6 == true){
    //     if(color1 == true){
    //         Friend1.classList.remove("white-element");
    //         Friend1.classList.add("info-element");
    //     }
    //     if(color2 == true){
    //         Friend2.classList.remove("white-element");
    //         Friend2.classList.add("info-element");
    //     }
    //     if(color3 == true){
    //         Friend3.classList.remove("white-element");
    //         Friend3.classList.add("info-element");
    //     }
    //     if(color4 == true){
    //         Friend4.classList.remove("white-element");
    //         Friend4.classList.add("info-element");
    //     }
    //     if(color5 == true){
    //         Friend5.classList.remove("white-element");
    //         Friend5.classList.add("info-element");
    //     }
    // }
}



function fenquRefreshA() {
    var a = document.getElementById("Alist"), b = document.getElementById("Blist"), c = document.getElementById("Clist"), d = document.getElementById("Dlist");
    a.style.display = "block";
    b.style.display = "none";
    c.style.display = "none";
    d.style.display = "none";

    document.getElementById("qushow").innerHTML = 'A区：XXXX'+'<span class="caret">'+'</span>';
    return;
}

function fenquRefreshB() {
    var a = document.getElementById("Alist"), b = document.getElementById("Blist"), c = document.getElementById("Clist"), d = document.getElementById("Dlist");
    a.style.display = "none";
    b.style.display = "block";
    c.style.display = "none";
    d.style.display = "none";

    document.getElementById("qushow").innerHTML = 'B区：XXXXX'+'<span class="caret">'+'</span>';
    return;
}

function fenquRefreshC() {
    var a = document.getElementById("Alist"), b = document.getElementById("Blist"), c = document.getElementById("Clist"), d = document.getElementById("Dlist");
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "block";
    d.style.display = "none";

    document.getElementById("qushow").innerHTML = 'C区：XXXXX'+'<span class="caret">'+'</span>';
    return;
}

function fenquRefreshD() {
    var a = document.getElementById("Alist"), b = document.getElementById("Blist"), c = document.getElementById("Clist"), d = document.getElementById("Dlist");
    a.style.display = "none";
    b.style.display = "none";
    c.style.display = "none";
    d.style.display = "block";

    document.getElementById("qushow").innerHTML = 'D区：XXXX'+'<span class="caret">'+'</span>';
    return;
}

$('#Aqu').on('click', fenquRefreshA);
$('#Bqu').on('click', fenquRefreshB);
$('#Cqu').on('click', fenquRefreshC);
$('#Dqu').on('click', fenquRefreshD);

//通过遍历给菜单项加上data-index属性

$(".atest").each(function (index) {
    if (!$(this).attr('data-index')) {
        $(this).attr('data-index', index);
    }
});

function aItem() {
    // 获取标识数据
    var dataUrl = $(this).attr('href'),
        dataIndex = $(this).data('index'),
        menuName = $.trim($(this).text());
    if(menuName.length>7){
        menuName = menuName.substr(0,7)+'...';
    }

    parent.window.aplus(dataUrl,dataIndex,menuName);
    return false;
}

$('.atest').on('click', aItem);


