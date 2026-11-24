# CUBEScape

**Project credit:** A coworker of mine came up with the original idea for this project.

Windows-oriented C# source for CubeScope, a Cisco Unified Border Element log and call-record analysis tool. The [manual](manual.html) describes log ingestion, calls, alerts, and the local dashboard. To read it in a browser, download the repository and open `manual.html`.

## Build and download status

The manual describes a .NET Framework 4.x build using `build.bat` and a single-file `CubeScope.exe`. This snapshot includes the C# files and dashboard HTML. The build script and executable are currently unavailable from this repository, so the manual's build steps require additional files.

Use authorized, sanitized logs when evaluating the tool. Remove call identifiers, phone numbers, and credentials before sharing samples.

## License

The source snapshot has no published reuse license. Confirm provenance and reuse terms with the maintainer before redistributing it.
