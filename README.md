[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub Release](https://img.shields.io/github/v/release/creagleone/dbtective)

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)

# About
Dbtective is a multi-approach database data comparison tool.

> [!IMPORTANT]  
> OracleDB thin mode only

<p align="center">
  <img src="src\gui\images\screens\compare_config.png" width="400">
  <img src="src\gui\images\screens\oracle_config.png" width="400">
</p>

## Database currently supported
| DB | Supported | Availability |
|--|--|--|
| Oracle | ✅ | 🆓 |
| CSV | ✅ | 🆓 |
| Others | ❌ | ❌ |

## OS currently supported
| OS | Supported |
|--|--|
| Windows | ✅ |
| Linux | ❌ |
| MacOS | ❌ |

# Features
| Feat | Description | Availability |
|--|--|--|
| Save Config | Ability to save database configurations | 🆓 |
| Tables filter | Ability to filter tables to compare | 🆓 |
| Compare by Hash | Calculate the hash of a file using the specified algorithm (Fast but without details) | 🆓 |
| Compare by Line | Retrieve the lines in deviations via the except clause (Depends on the size of the databases to be compared) | 🆓 |
| Compare by Column | Retrieve the columns in deviations via the Levenshtein distance (Depends on the size of the databases to be compared) | 🆓 |

# Translations
| Language | Status |
|--|--|
| English | ✅ |
| French | ✅ |
| Others | ❌ |

# Documentations
See [documentation](https://creagleone.github.io/dbtective/)

# Downloads
Click on [Github release](https://github.com/creagleone/dbtective/releases/latest)

# Credits
Based on [PyOneDark](https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI) ([Wanderson-Magalhaes](https://github.com/Wanderson-Magalhaes))