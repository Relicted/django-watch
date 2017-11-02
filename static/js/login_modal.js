$(document).ready(function () {
    $('.like-btn').each(function () {
       $(this).attr('data-toggle', 'modal');
       $(this).attr('data-target', '#login-modal')
    });

    $('.video-settings').each(function () {
       $(this).attr('data-toggle', 'modal');
       $(this).attr('data-target', '#login-modal');
    });

    $('.user-menu').each(function () {
       $(this).attr('data-toggle', 'modal');
       $(this).attr('data-target', '#login-modal');
    });

    $('[data-action="like"]').each(function () {
        $(this).removeAttr('data-action')
    });
    $('[data-action="dislike"]').each(function () {
        $(this).removeAttr('data-action')
    })
});

