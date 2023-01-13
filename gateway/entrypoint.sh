#!/bin/bash

export RESTY_CONF_DIR="/usr/local/openresty/nginx/conf"
export NGINX_CONF_DIR="/etc/nginx/conf.d"
export GATEWAY_SERVERS_CONFIG_FILE="/gateway.json"

# openresty will change it later on his own, right now we're just giving it access
chmod 777 /etc/resty-auto-ssl

# we want to keep dhparam.pem in volume, to generate just one time
if [ ! -f "/etc/resty-auto-ssl/dhparam.pem" ]; then
  if [ -n "$DIFFIE_HELLMAN" ]; then
    openssl dhparam -out /etc/resty-auto-ssl/dhparam.pem 2048
  else
    cp ${RESTY_CONF_DIR}/dhparam.pem /etc/resty-auto-ssl/dhparam.pem
  fi
fi


if [ -f $GATEWAY_SERVERS_CONFIG_FILE ]; then
  python3 generate_server_confs.py
# if $SITES isn't defined, let's check if $NGINX_CONF_DIR is empty
elif [ ! "$(ls -A ${NGINX_CONF_DIR})" ]; then
  # if yes, just copy default server (similar to default from docker-openresty, but using https)
  cp ${RESTY_CONF_DIR}/server-default.conf ${NGINX_CONF_DIR}/default.conf
fi


if [ "$FORCE_HTTPS" == "true" ]; then
  # only do this, if it's first run
  if ! grep -q "force-https.conf" ${RESTY_CONF_DIR}/resty-server-http.conf
  then
    echo "include force-https.conf;" >> ${RESTY_CONF_DIR}/resty-server-http.conf
  fi
fi


# let's substitute $ALLOWED_DOMAINS, $LETSENCRYPT_URL and $RESOLVER_ADDRESS into OpenResty configuration
envsubst '$ALLOWED_DOMAINS,$LETSENCRYPT_URL,$RESOLVER_ADDRESS,$STORAGE_ADAPTER,$REDIS_HOST,$REDIS_PORT,$REDIS_DB,$REDIS_KEY_PREFIX' \
  < ${RESTY_CONF_DIR}/resty-http.conf \
  > ${RESTY_CONF_DIR}/resty-http.conf.copy \
  && mv ${RESTY_CONF_DIR}/resty-http.conf.copy ${RESTY_CONF_DIR}/resty-http.conf

exec "$@"