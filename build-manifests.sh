#!/bin/bash -ex

main() {
    local dirs
    dirs=($(find . -name kustomization.y?ml -printf "%h\n"))
    local out=auto-generated
    local ret=0
    rm -rf "$out"
    mkdir -p "$out"

    for d in "${dirs[@]}"; do
        o="${out}/${d}"
        mkdir -p "$o"
        if ! kustomize build -o "$o" "$d"; then
            echo "failed to build $d" >&2
            ret=1
        fi
    done

    exit "$ret"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
