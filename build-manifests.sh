#!/bin/bash -ex

main() {
    local dirs
    dirs=($(find . -name kustomization.y?ml -printf "%h\n"))
    local out=auto-generated
    rm -rf "$out"
    mkdir -p "$out"

    for d in "${dirs[@]}"; do
        o="${out}/${d}"
        mkdir -p "$o"
        if ! kustomize build -o "$o" "$d"; then
            echo "failed to build $d" >&2
        fi
    done
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
