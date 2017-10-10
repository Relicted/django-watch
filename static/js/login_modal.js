$(document).ready(function () {
    $('.video-like-btn').each(function () {
       $(this).attr('data-toggle', 'modal');
       $(this).attr('data-target', '#login-modal')
    });

    $('.video-settings').each(function () {
       $(this).attr('data-toggle', 'modal');
       $(this).attr('data-target', '#login-modal');
    });
});