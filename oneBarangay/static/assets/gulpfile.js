/*

=========================================================
* Volt Free - Bootstrap 5 Dashboard
=========================================================

* Product Page: https://themesberg.com/product/admin-dashboard/volt-premium-bootstrap-5-dashboard
* Copyright 2020 Themesberg (https://www.themesberg.com)
* License (https://themesberg.com/licensing)

* Designed and coded by https://themesberg.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. Please contact us to request a removal.

*/

const autoprefixer = require('gulp-autoprefixer')
const browserSync = require('browser-sync').create()
const cleanCss = require('gulp-clean-css')
const del = require('del')
const htmlmin = require('gulp-htmlmin')
const cssbeautify = require('gulp-cssbeautify')
const gulp = require('gulp')
const npmDist = require('gulp-npm-dist')
const sass = require('gulp-sass')(require('node-sass'))
const wait = require('gulp-wait')
const sourcemaps = require('gulp-sourcemaps')
const fileinclude = require('gulp-file-include')
const rename = require('gulp-rename')

// Define paths

const paths = {
  dist: {
    base: './dist/',
        css: "./dist/css",
    html: './dist/pages',
    assets: './dist/assets',
    img: './dist/assets/img',
    vendor: './dist/vendor'
  },
  dev: {
    base: './html&css/',
    css: './html&css/css',
    html: './html&css/pages',
    assets: './html&css/assets',
    img: './html&css/assets/img',
    vendor: './html&css/vendor'
  },
  base: {
    base: './',
    node: './node_modules'
  },
  src: {
    base: './',
    css: './css',
    html: './src/pages/**/*.html',
    assets: './src/assets/**/*.*',
    partials: './src/partials/**/*.html',
    scss: './scss',
    node_modules: './node_modules/',
    vendor: './vendor'
  },
  temp: {
    base: './.temp/',
    css: './.temp/css',
    html: './.temp/pages',
    assets: './.temp/assets',
    vendor: './.temp/vendor'
  }
}

// Compile SCSS
gulp.task('scss', function () {
  return gulp
    .src([paths.src.scss + '/custom/**/*.scss', paths.src.scss + '/volt/**/*.scss', paths.src.scss + '/volt.scss'])
    .pipe(wait(500))
    .pipe(sourcemaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(
      autoprefixer({
        overrideBrowserslist: ['> 1%']
      })
    )
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.src.css))
    .pipe(browserSync.stream())
})

// Minify CSS
gulp.task('minify:css', function () {
  return gulp
    .src([paths.src.css + '/volt.css'])
    .pipe(cleanCss())
    .pipe(
      rename(function (path) {
        // Updates the object in-place
        path.extname = '.min.css'
      })
    )
    .pipe(gulp.dest(paths.src.css))
})

// Default
gulp.task('default', gulp.series('scss', 'minify:css'))
