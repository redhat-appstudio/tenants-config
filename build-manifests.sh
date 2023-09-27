#!/bin/bash -e

main() {
    local dirs
    dirs=($(find cluster -maxdepth 4 \( -name 'kustomization.yaml' -o -name 'kustomization.yml' \) | xargs dirname))
    local out=auto-generated
    local ret=0
    rm -rf "$out"
    mkdir -p "$out"

    for d in "${dirs[@]}"; do
        echo "Checking directory ${d}"
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
