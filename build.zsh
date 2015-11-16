echo 'Step 0: Kill ALL THE THINGS... in `dist/`'

rm -rf dist/*

echo 'Step 1: Copy all the HTML'
cp src/embedTFW.html dist/
mkdir dist/partials/
cp -r src/partials dist/

echo 'Step 2a: Build all the Sass into CSS!'
npm run sass

echo 'Step 2b: Copy CSS into `dist/`?'
mkdir dist/css/
cp src/css/main.css dist/css/

mkdir dist/audio/
cp src/audio/tanks8bit.wav dist/audio/

echo 'Step 3: Copy all the JS'
mkdir -p dist/js && cp -r src/js dist/

# echo 'Step 3: Copy the IMG folde'
# mkdir -p dist/img && cp -r src/img dist/

echo 'Step 4: Copy all the `bower_components/`!'

echo 'Step 4a: Normalize the CSS...'
mkdir -p dist/bower_components/normalize-css/
cp bower_components/normalize-css/normalize.css dist/bower_components/normalize-css/normalize.css

echo 'Step 4b: ????'
mkdir -p dist/bower_components/jquery/dist/
cp bower_components/jquery/dist/jquery.js dist/bower_components/jquery/dist/jquery.js

mkdir -p dist/bower_components/angular/
cp bower_components/angular/angular.js dist/bower_components/angular/angular.js

mkdir -p dist/bower_components/angular-route/
cp bower_components/angular-route/angular-route.js dist/bower_components/angular-route/angular-route.js

mkdir -p dist/bower_components/modernizr/src/
cp bower_components/modernizr/modernizr.js dist/bower_components/modernizr/modernizr.js

mkdir -p dist/bower_components/font-awesome/css/
cp bower_components/font-awesome/css/font-awesome.min.css dist/bower_components/font-awesome/css/font-awesome.min.css

mkdir -p dist/bower_components/firebase/
cp bower_components/firebase/firebase.js dist/bower_components/firebase/firebase.js

mkdir -p dist/bower_components/angularfire/dist/
cp bower_components/angularfire/dist/angularfire.min.js dist/bower_components/angularfire/dist/angularfire.min.js

npm start
