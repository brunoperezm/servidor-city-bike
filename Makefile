deploy:
	heroku container:push web --app citybikeserver
	heroku container:release web --app citybikeserver
build:
	docker build -t flask-heroku:latest .
run:
	docker run -e DEBUG='yes' -p 5000:5000 flask-heroku 
