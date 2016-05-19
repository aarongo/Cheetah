#!/usr/bin/env bash

FIND_DIR="/software/upload_project/"
IMAGES_PATH="assets/upload"
STATIC_PATH="www"

find ./ -name "*cybershop-mobile-0.0.1*" -type d

discover () {
    find  ${FIND_DIR} -mtime +3 -name "*cybershop-mobile-0.0.1*" |sort -r > /software/old_protject.txt
}

unlink () {
    cat "/software/old_protject.txt" | while read line
    do
        rm -f  ${line}/${IMAGES_PATH}
        rm -f ${line}/${STATIC_PATH}
    done
}
delete () {
    cat "/software/old_protject.txt" | while read line
    do
        rm -rf  ${line}
    done

}

discover
unlink
delete