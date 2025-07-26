# ATLYSS Template Mod

This is a VS 2022 project that can be used as a basis for making BepInEx 5 plugins for ATLYSS.

This template is targeted towards publishing mods with Thunderstore, and will generate a ZIP package for it upon building.

# Configuring the project

Set the following properties in [Directory.Build.props](./Directory.Build.props):
- `AtlyssPath` - **IMPORTANT** - the install path for Atlyss on your machine, used to reference the game assembly
- `CreateThunderstorePackage` - `true` to generate a Thunderstore package, `false` to skip it; usually you want this set to `true`
- `ThunderstorePackageName` - the name of the package; used as the `name` field in `manifest.json`, and is part of the generated ZIP name
- `ThunderstoreTeamName` - the team used for publishing this package; this should match the team that you normally use to upload to Thunderstore, and is part of the generated ZIP name
  - while not normally required, specifying this correctly allows you to install the mod locally without having to specify the author every time
- `ThunderstorePackageDescription` - the description for the package; used as the `description` field in `manifest.json`
- `ThunderstoreWebsite` - a link to a git repository, website, contact page, etc.; used as the `website` field in `manifest.json`
- `ThunderstoreDependency` - a dependency string for a package from Thunderstore; all `ThunderstoreDependency` items are combined and used as the `dependencies` field in `manifest.json`
- `ThunderstoreAssemblyInclude` - an assembly to copy over to the generated ZIP package; by default, the generated plugin assembly is included
  - you should include any third-party or runtime dependencies that don't come from Thunderstore dependencies, or aren't bundled with ATLYSS itself 

Also set the following properties in the project file for the plugin:
- `AssemblyName` - name of the generated plugin assembly, also used as the GUID of the plugin
- `Product` - used as the name of the plugin
- `Version` - used as the version of the plugin and the `version` field in `manifest.json`

# Distributing on Thunderstore

You can distribute your mod on Thunderstore by uploading the generated ZIP package.

Before uploading, double check that the ZIP package contains the correct files (manifest.json, icon.png, README.md, CHANGELOG.md) and has only the strictly necessary assemblies in the "plugins" folder.

# Testing locally using r2modman

You can use the "Import local mod" in r2modman options to import your generated ZIP package.

This allows you to test your mod, and check that it will work properly for people who install it from Thunderstore.

![](https://i.imgur.com/qAsRVyA.png)

# Best practices

- Describe your mod in the README.md Thunderstore file, and add some form of contact info for people who want to report bugs or give suggestions
- Increment your `Version` property in the project every time you want to upload an update according to Semantic Versioning rules: https://semver.org/
- Do not change the `ThunderstorePackageName` after uploading your mod; if you do, Thunderstore will see it as a new, unique mod, instead of updating your old submission
- Set `ThunderstoreTeamName` as the name of the team you use to upload the mod on Thunderstore, and don't change it

# Contributors

- [nyxical420](https://github.com/nyxical420)