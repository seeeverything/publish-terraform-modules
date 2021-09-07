# Publish Terraform Modules 

This GitHub action publishes modules to a Terraform Registry by interacting with the [Terraform Registry API](https://www.terraform.io/docs/registry/api.html) and the [Registry Modules Api](https://www.terraform.io/docs/cloud/api/modules.html)

# Usage 

```
- uses: seeeverything/publish-terraform-modules@1.0.0
  with:
    # List of modules to publish, each module has to be a folder in the root repository. 
    modules_list: '[]'

    # Module provider
    # Default: aws
    provider: "aws"

    # Terraform Registry organization or namespace     
    namespace: ""

    # API Token used to access the Terraform Registry
    # We recommend using a repository or organization secret to store the Token
    # e.g ${{ github.TF_API_TOKEN }}
    token: ''

    # Wheter to recreate to override a module version if that one already exists
    #
    # Default: false
    recreate: "false"

    # Base version to use if the module has no versions or autbump is false
    #
    # Default: 1.0.0
    base_version: "1.0.0"

    # Whether to bump the module patch version or use the `base_version` as default
    #
    # Default: true
    autobump: "true"
```

# Example

The following example will:
- Check out a repository
- Get the root folders for the files modified in the current commit
- Publish a new version for each folder as a terraform module

```
name: publish-modules

on:
  push:
    branches: [master]

jobs: 
  publish-modules:    
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: get-files-changed
        id: get-files-changed
        run: |
          files="$(git diff-tree --no-commit-id --name-only -r ${{ github.sha }})"
          folders_list="[]"

          for file in $files
          do  
            folder="$(echo $(dirname "${file}") | sed 's!/*\([^/]*\).*!\1!g')"
            folders_list="$(echo "$folders_list" | jq ". += [\"$folder\"]")"
          done

          unique_list="$(echo "$folders_list" | jq -c unique )"
          echo "::set-output name=FOLDERS_LIST::$unique_list"

      - name: publish
        if: github.ref == 'refs/heads/master' && github.event_name == 'push'
        uses: seeeverything/publish-terraform-modules@1.0.0
        with:
          modules_list: ${{ steps.get-files-changed.outputs.FOLDERS_LIST }}
          provider: "aws"
          namespace: "organization"
          token: ${{ secrets.TF_CLOUD_API_TOKEN }}
          recreate: "false"
          base_version: "1.0.0"
          autobump: "true"
```
