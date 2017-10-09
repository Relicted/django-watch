$(document).ready(function () {


    //MAGNIFIC  SCREANSHOTS AND POSTER
    $('.item').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        },
         removalDelay: 50,
         mainClass: 'mfp-fade'

    });

    $('.poster').magnificPopup({
        delegate: 'a',
        type: 'image'
    });


    $("#id_avatar").on('change', function () {
            validExt = ['jpg', 'png', 'gif'];
            fileName = this.files[0].name;
            fileExt = this.files[0].name.split('.').pop();
            if (validExt.indexOf(fileExt) === -1 ){
                document.getElementById('profile-pic-error').textContent = 'We only support PNG, GIF, or JPG pictures.'
            } else {
                $("#profile-pic-modal").modal('show')

            }
        });

    // VIDEO ADD BUTTONS
    $('.video-controls').on('click', function () {
    $(this).toggleClass("animated shake go");
    $('.controls-btns ul').toggleClass('opened');
    $('.controls-add').toggleClass('go')
    });



    $('form[name="login-modal"]').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            url: "/account/login/",
            type: 'POST',
            data: {
                username: $('input[name="username"]').val(),
                password: $('input[name="password"]').val(),
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()

            },
            success: function (data) {
                if (data) {
                    if (data.password) {
                        $('#password-errors').html(data.password);
                        $('#id_password').parent().addClass('has-error')
                    } else if (data.username) {
                        $('#username-errors').html(data.username);
                        $('#id_username').parent().addClass('has-error')
                    } else if(data['reload']) {
                        location.reload()
                    }
                }
            }
        })
    });


    $('form[name="login-modal"] .form-control').on('focus', function () {
        $(this).parent().removeClass('has-error');
        $('.errorlist').html('')
    });



    $('.serial-list .bck').mouseenter(function () {
        var item = $(this).parent();
        var id = $(this).attr('id').replace('video-', '');
        var timer = setTimeout(function(){after2(id, item)}, 700);
        $(this).mouseleave(function () {
            clearTimeout(timer);
            $('#item-fast-info').removeAttr('style')

        });
        $('.video-settings').on('click', function () {
            clearTimeout(timer);
        })
    });

    function after2(id, item){
        $.ajax({
            url: `/video/item/${id}/`,
            type: 'GET',
            data: {'id': id},
            success: function (data) {
                let left, top, container, toLeft, vidItem, toRight, style;

                left = Math.trunc(item.position().left);
                top = Math.trunc(item.position().top);
                container = $('.serial-list').width();
                toLeft = container - left + 20;
                vidItem = item.width();
                toRight = left + vidItem - 10;

                if (left > container / 2) {
                    style = `top:${top}px;right:${toLeft}px;display:block;visibility:visible;z-index:20;opacity:1`
                }

                else if (left < container / 2) {
                    style = `top:${top}px;left:${toRight}px;display:block;visibility:visible;z-index:20;opacity:1`
                }

                $("#item-fast-info").attr('style', style);
                $('.fast-description').text(data.response['description']);
                $('.like-btn.up span').text(data.response['like']);
                $('.like-btn.down span').text(data.response['dislike']);

                $('#item-fast-info').mouseenter(function () {

                    $(this).attr('style', style);
                    $(this).mouseleave(function () {
                        $(this).removeAttr('style')
                    });
                });
            }
        });
    }



});



