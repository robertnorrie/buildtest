# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/properties/compilers/properties/compiler/properties/gcc
```

Declaration of one or more GNU compilers where we define C, C++ and Fortran compiler. The GNU compiler wrapper are `gcc`, `g++` and `gfortran`. 


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## gcc Type

`object` ([Details](settings-properties-compilers-properties-compiler-properties-gcc.md))

# undefined Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                                         |
| :------- | -------- | -------- | -------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section.md "settings.schema.json#/properties/compilers/properties/compiler/properties/gcc/patternProperties/^.\*$") |

## Pattern: `^.*$`

A compiler section is composed of `cc`, `cxx` and `fc` wrapper these are required when you need to specify compiler wrapper.


`^.*$`

-   is optional
-   Type: `object` ([Details](settings-definitions-compiler_section.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section.md "settings.schema.json#/properties/compilers/properties/compiler/properties/gcc/patternProperties/^.\*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-compiler_section.md))