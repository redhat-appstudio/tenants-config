#!/bin/bash -e

main() {
    local target_dir=${1:?target dir for storing kustomize should be specified}
    
    mkdir -p "$target_dir"
    if [[ -f "${target_dir}/kustomize" ]]; then
        exit 0
    fi

    curl -L https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.3.0/kustomize_v5.3.0_linux_amd64.tar.gz | tar -C "$target_dir" -xvzf -

    ls -l "$target_dir"
    echo "PATH -> $PATH"
}


if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi


