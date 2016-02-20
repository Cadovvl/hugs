#!/bin/bash

rm -f /etc/init.d/hugs
/sbin/initctl reload-configuration
