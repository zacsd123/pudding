$(document).ready(function () {
    get_comment_list();
});

function webStorage(id) {
    data = JSON.parse(localStorage.getItem('gId'));
    if (data == '' | data == null) {
        data = [];
    }
    if (data.includes(id)) {
        alert("추천은 한 번만 가능합니다.");
        return false;
    } else {
        data.push(id);
        localStorage.setItem('gId', JSON.stringify(data));
    }
    return true;
}


function addGood(id) {
    if ('6413ffa7908f78a240fbf0b0' == "") {
        console.log($("#btnLogin"))
        $("#loginModal").modal('show');
    } else {
        if (webStorage(id)) {
            $.ajax({
                url: "/board/add_good",
                type: "POST",
                data: {
                    "id": id,
                    "csrf_token": "IjRhNDQ4MzE2MGUzMTI0NWNjMDJmODU0ZWZkMjQ3NDAzN2EwOWMyN2Qi.ZBlRSg.obVZpWBS1tsFBmUOXmOrOJ6-9l4",
                },
                success: function (error) {
                    $("#bgood").html(Number($("#bgood").text()) + 1);
                    get_comment_list();

                },
                error: function (request, status, error) {
                    var msg = "Error : " + request.status + "<br>";
                    msg += "내용 : " + request.responseText + "<br>" + error;
                    console.log(msg);
                }
            });
        } else {
            return false
        }
    }
}

function addComment() {

    if ($.trim($("#comment").val()) == "") {
        alert("댓글 내용을 입력하세요.");
        $("#comment").focus();
        return false;
    }

    $.ajax({
        url: "/board/comment_write",
        type: "POST",
        data: $("#commentForm").serialize(),
        success: function (data) {
            $("#comment").val("");
            get_comment_list();
        },
        error: function (request, status, error) {
            var msg = "Error : " + request.status + "<br>";
            msg += "내용 : " + request.responseText + "<br>" + error;
            console.log(msg);
        }
    });
}

function deleteComment(idx) {
    $.ajax({
        url: "/board/comment_delete",
        type: "POST",
        cache: false,
        async: false,
        data: {
            "id": idx,
            "csrf_token": "IjRhNDQ4MzE2MGUzMTI0NWNjMDJmODU0ZWZkMjQ3NDAzN2EwOWMyN2Qi.ZBlRSg.obVZpWBS1tsFBmUOXmOrOJ6-9l4",
        },
        success: function (data) {
            if (data["error"] == "success") {
                get_comment_list();
            }
        },
        error: function (request, status, error) {
            var msg = "Error : " + request.status + "<br>";
            msg += "내용 : " + request.responseText + "<br>" + error;
            console.log(msg);
        },
    });
}

function editCommentOK(idx) {
    var new_comment = $("#i" + idx).val();
    $.ajax({
        url: "/board/comment_edit",
        type: "POST",
        cache: false,
        data: {
            "id": idx,
            "csrf_token": "IjRhNDQ4MzE2MGUzMTI0NWNjMDJmODU0ZWZkMjQ3NDAzN2EwOWMyN2Qi.ZBlRSg.obVZpWBS1tsFBmUOXmOrOJ6-9l4",
            "comment": new_comment,
        },
        success: function (data) {
            if (data["error"] == "success") {
                get_comment_list();
                alert("수정 완료되었습니다.")
            }
        },
        error: function (request, status, error) {
            var msg = "Error : " + request.status + "<br>";
            msg += "내용 : " + request.responseText + "<br>" + error;
            console.log(msg);
        }
    })
}


function editComment(idx) {
    var html = "";
    var comment = $("#t" + idx).data("comment");
    html += "<textarea row=3 class='form-control' style='width: 100%;' id='i" + idx + "'>" + comment;
    html += "</textarea>";
    html += "<a href='#;return false;' style='position: relative; top:-95px; left: 80px;' class='btn btn-outline-primary btn-sm' onclick='editCommentOK(\"" + idx + "\")'>저장</a>";
    html += "<a href='#;return false;' style='position: relative; top:-95px; left: 80px;' class='btn btn-outline-secondary ms-2 btn-sm' onclick='cancelEdit(\"" + idx + "\")'>취소</a>";
    $("#t" + idx).html(html);
}

function cancelEdit(idx) {
    var comment = $("#t" + idx).data("comment");
    $("#t" + idx).html(comment);
}

function get_comment_list() {
    $.ajax({
        url: "/board/comment_list/6409e873edaecdd782ce7848",
        type: "GET",
        cache: false,
        dataType: "json",
        success: function (data) {
            c = data.lists;
            html = "";
            if (c.length > 0) {
                for (var i = 0; i < c.length; i++) {
                    html += "<div>";
                    html += "<table class='table table-borderless table-sm' style='border-color: #eee;'>";
                    html += "<tr>"
                    html += "<td colspan='2' style='font-size: 13px;'><span style='color: #0af;'>" + c[i].job + "</span> · " + c[i].email + "</td>"
                    html += "</tr>"
                    html += "<tr>"
                    html += "<td id='t" + c[i].id + "' data-comment='" + c[i].comment + "'>" + c[i].comment + "</td>";
                    if (c[i].owner) {
                        html += "<td width='108px' style='text-align: right;'>"
                        html += "<a class='btn btn-outline-secondary btn-sm' href='#;return false;' onclick='editComment(\"" + c[i].id + "\")'>수정</a>";
                        html += "<a class='btn btn-outline-danger ms-2 btn-sm' href='#;return false;' onclick='deleteComment(\"" + c[i].id + "\")'>삭제</a>";
                        html += "</td>"
                    }
                    html += "</td>";
                    html += "<tr>"
                    html += "<td class='text-right' style='font-size: 13px; color: #888;'>"
                    html += '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16" style="position: relative; top:-1px">'
                    html += '<path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/></svg> '
                    html += c[i].pubdate;
                    html += "<a href='#;return false;' onclick='addGood(\"c" + c[i].id + "\")' style='text-decoration: none; color: #888;'>"
                    html += '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" class="bi bi-hand-thumbs-up ms-3" viewBox="0 0 16 16" style="position: relative; top:-2px">'
                    html += '<path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/></svg> '
                    html += c[i].good + "</a>";

                    html += "</tr>";
                    html += "</table>";
                    html += "</div>";
                }

            }
            $(".cCnt").html(c.length);
            $("#commentList").html(html);
        },
        error: function (request, status, error) {
            var msg = "Error : " + request.status + "<br>";
            msg += "내용 : " + request.responseText + "<br>" + error;
            console.log(msg);
        }
    })
}