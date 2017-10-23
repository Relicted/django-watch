'use strict';

const gulp         = require('gulp'),
      sass         = require('gulp-sass'),
      browserSync  = require('browser-sync'),
      concat       = require('gulp-concat'),
      uglify       = require('gulp-uglifyjs'),
      cssnano      = require('gulp-cssnano'),
      rename       = require('gulp-rename'),
      del          = require('del'),
      imagemin     = require('gulp-imagemin'),
      pngquant     = require('imagemin-pngquant'),
      cache        = require('gulp-cache');


gulp.task('sass', function () {
    return gulp.src("static/sass/**/*.sass")
        .pipe(sass())
        .pipe(gulp.dest('static/css'))
        .pipe(browserSync.reload({stream: true}))
});

gulp.task('scripts', function () {
    return gulp.src([
        'static/libs/jquery.js',
        'static/libs/mp/dist/jquery.magnific-popup.min.js',
        'static/libs/bootstrap/js/bootstrap.js',
        'static/libs/animateit/js/css3-animate-it.js',
    ])
        .pipe(concat('libs.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('static/js'));
});

gulp.task('css-libs', ['sass'], function () {
    return gulp.src('app/css/libs.css')
        .pipe(cssnano())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('static/css'));
});

gulp.task('clear', function () {
    return cache.clearAll();
});


gulp.task('watch', ['css-libs', 'scripts'], function () {
    browserSync.init({
        notify: false,
        proxy: "localhost:8000"
    });
    gulp.watch('static/sass/**/*.sass', ['sass']);
    gulp.watch('templates/**/*.html', browserSync.reload);
    gulp.watch('static/js/**/*.js', browserSync.reload);
});


gulp.task('clean', function () {
   return del.sync('build')
});

gulp.task('build', ['clean', 'sass', 'scripts'], function () {
    var buildCss = gulp.src(['static/css/main.css', 'app/css/libs.min.css'])
        .pipe(gulp.dest('build/css'));

    var buldFonts = gulp.src('static/fonts/**/*')
        .pipe(gulp.dest('build/fonts'));

    var buildJs = gulp.src('static/js/**/*.js')
        .pipe(gulp.dest('build/js'));

});
