FROM node:14.14.0-stretch as build
WORKDIR /app

COPY . ./

RUN npm install \
	&& npm run build

FROM nginx
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80