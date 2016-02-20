#!/bin/bash

rm -f ./res/config.js
rm -f ./res/config.json

export LOCATE=$(cat ./res/location)
ln -s ./res/config_${LOCATE}.js ./res/config.js
ln -s ./res/config_${LOCATE}.json ./res/config.json

if [ "${LOCATE}" == "prod" ];
then
    cp -f ./upstart.conf /etc/init/hugs.conf
    ln -sf /lib/init/upstart-job /etc/init.d/hugs
    /sbin/initctl reload-configuration
fi;