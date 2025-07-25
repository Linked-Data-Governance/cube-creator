# Cube Creator User Guide

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Workflow](#step-by-step-workflow)
   - [Data Preparation](#step-0-data-preparation)
   - [CSV Mapping](#step-1-csv-mapping)
   - [Transformation](#step-2-transformation)
   - [Cube Designer](#step-3-cube-designer)
   - [Publication](#step-4-publication)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)

## Overview

Cube Creator transforms your CSV data into semantic RDF data cubes that can be published and visualized on platforms like visualize.admin.ch and opendata.swiss. The tool ensures your data follows W3C Data Cube standards and includes proper metadata for discoverability and reuse.

## Prerequisites

Before starting with Cube Creator, ensure you have:

- Access to the [Cube Creator platform](https://test.cube-creator.lindas.admin.ch/) 
- CSV data files prepared according to the requirements
- Basic understanding of your data structure and dimensions
- Knowledge of the target publication platforms (visualize.admin.ch, opendata.swiss and LINDAS to query your data through SPARQL)

## Step-by-Step Workflow

### Step 0: Data Preparation

**Purpose**: Prepare your input data in valid CSV format that meets Cube Creator requirements. You can can validate your with the [CSV validation tool](https://zazuko.com/csv-validate/).

#### Basic Requirements

- ✅ **UTF-8 Encoding**: All CSV files must use UTF-8 encoding, if you're on Windows, you can use Notepad to detect and change encoding
- ✅ **No Empty Lines**: Remove empty lines, especially at the end of files
- ✅ **Syntactic Validity**: Follow RFC4180 standards
  - Use commas as delimiters (preferred)
  - Quote strings containing commas or quotes
  - Double quotes within strings: `"Hans ""Johnny"" Müller"`
- ✅ **No Umlauts in Filenames**: Avoid special characters (ä, ö, ü) in CSV filenames

#### Data Formats

| Data Type | Format                  | Example                 |
| --------- | ----------------------- | ----------------------- |
| Date      | YYYY-MM-DD              | `2001-01-31`          |
| DateTime  | YYYY-MM-DDThh:mm:ss     | `2001-01-31T17:30:00` |
| Time      | hh:mm:ss                | `21:32:52`            |
| Boolean   | true/false              | `true`, `false`     |
| Decimal   | Use . as separator      | `123.456`             |
| Integer   | No thousands separators | `-2147483648`         |

#### Tips for Excel Users

- Change system delimiter settings for consistent CSV export
- Consider data transposition if you have cross-tabulated data
- Use the [CSV validation tool](https://zazuko.com/csv-validate/) to check syntax

### Step 1: CSV Mapping

**Purpose**: Upload CSV files and map them to cube dimensions and tables.

#### Key Concepts

- **Dimensions**: Categories that organize your data (e.g., geography, time, measurements). They correspond to the columns in the CSV file
- **Cube Table**: The main table containing observations and dimensions. It describes the structure of your cube
- **Shared Dimensions**: Represents the concepts that are used over and over in many cubes. These concepts or terms can be reused inside your data cubes. Shared dimensions allows us to **link** our data to other existing data in LINDAS
- **Concept Tables**: Additional tables for multilingual labels and metadata. A concept table is the possibility to handle the values of a dimension as a URL to a new ressource (a concept). This is similar to an object that is the URL of a Shared Dimension's term but here the concepts are created for the cube and uploaded with the cube

#### Workflow

1. **Upload CSV Files**

   - Click "+" to upload syntactically valid CSV files
   - Preview columns and first three rows
   - Multiple CSV files can be uploaded for complex cubes
2. **Create Tables**

   **Cube Table (Required)**

   - Select the columns/dimensions that you would like to include in the generated RDF cube. Check "Cube table" checkbox for your main data table
   - Contains observations with key and measurement dimensions
   - Must distinguish between different dimension types

   **Concept Tables (Optional)**

   - Create for multilingual concepts. Select the columns that you would like to include in the concept table. A concept table is created without checking the "Cube table" checkbox
   - Link to cube table using "Link to another table". This allows us to link a dimension to a concept (to treat the values of a dimension as a resource)
   - Provide translations and additional metadata
3. **Configure Table Settings**

   **Identifier Template**

   - Creates unique URIs for each row
   - Use format: `table-name/{column1}/{column2}`. Recommandation : use columns that have values that do not contain special characters
   - Auto-complete available with `{` trigger
   - Leave empty for auto-generated identifiers

   **Display Color**

   - Visual connection between CSV inputs and mapped tables
   - Used only within Cube Creator interface
4. **Map Columns**

   **Target Properties**

   - For Cube Tables: Dimension properties
   - For Concept Tables: `schema:name`, `schema:description`, `schema:position`
   - Auto-complete for common ontologies (e.g., "schema"). This is the list of preloaded ontologies in cube creator : [rdfs](https://prefix.zazuko.com/prefix/rdfs), [schema](https://prefix.zazuko.com/prefix/schema),[qb](https://prefix.zazuko.com/prefix/qb), [sdmx](https://prefix.zazuko.com/prefix/sdmx), [dcterms](https://prefix.zazuko.com/prefix/dcterms), [cd11](https://prefix.zazuko.com/prefix/dc11), [skos](https://prefix.zazuko.com/prefix/skos), [skosxl](https://prefix.zazuko.com/prefix/skosxl), [xskos](https://prefix.zazuko.com/prefix/xkos), [xsd](https://prefix.zazuko.com/prefix/xsd), [wgs](https://prefix.zazuko.com/prefix/wgs).

   **Data Types**

   - Choose appropriate type for validation
   - Critical for measurement dimensions
   - Transformation fails on type mismatches

   **Language Settings**

   - Specify language for string dimensions
   - Use concept tables for multilingual content
   - `schema:name` mandatory in concept tables

   **Default Values**

   - Handle missing values with meaningful defaults
   - Prevents explicitly missing values in final cube

### Step 2: Transformation

**Purpose**: Convert mapped CSV data into RDF cube format.

#### Process

1. **Start Transformation**

   - Click "Start transformation" button after mapping completion
   - Monitor progress with status indicators:
     - Grey: Pending
     - Blue (blinking): Running
     - Red: Failed
     - Green: Successful
2. **Monitor Jobs**

   - View transformation history
   - Access detailed logs for debugging
   - Check error messages for failed transformations
3. **Handle Errors**

   - **Invalid Datatype**: Data doesn't match selected type
   - Check error line numbers in logs
   - Verify data format matches dimension settings
4. **Replace CSV (Optional)**

   - Update cube with new data
   - Same separator character required
   - Column names must match (case-sensitive)
   - All original columns must be present

💡 **Tip**: Use sample CSV files for initial testing to avoid long wait times with large datasets.

### Step 3: Cube Designer

**Purpose**: Add metadata, verify data correctness, and prepare for publication. A dimension must have a Scale of measure.

#### Metadata Configuration

**Dataset/Cube Metadata**

- Access via 🖊️ icon next to cube title
- Complete all required fields
- Provide multilingual descriptions

**Status Settings**

- **Draft**: Shows in applications as draft status
- **Published**: Supersedes draft versions
- Choose publication targets (visualize.admin.ch, opendata.swiss)

**Dimension Metadata**

- Click 🖊️ for each dimension column

**Essential Fields:**

- **Name**: Descriptive name for the dimension
- **Description**: Detailed explanation of dimension content
- **Dimension Type**:
  - Measurement: Contains data values/observations
  - Key: Used for filtering for instance in visualize.admin.ch (cannot be deleted by users)
  - Optional: Available as optional filter

**Scale of Measure**

- **Nominal**: Named categories (e.g., cantons, colors)
- **Ordinal**: Ordered categories (e.g., small, medium, large)
- **Interval**: Proportional intervals (e.g., temperature in Celsius)
- **Ratio**: Has meaningful zero point (e.g., mass)

**Units** (for Measurement Dimensions)

- Select from QUDT-based unit list
- Use "Number (#)" for counts
- Use "Percent (%)" for percentages

**Data Kind** (Optional)

- Geographic coordinates: For lat/long data
- Geographic shape: For shape data from Shared Dimensions
- Time description: For temporal data types

#### Linking to Shared Dimensions

- Available for nominal/ordinal concepts
- Click 🔗 symbol to map to existing concept hierarchies
- Enables geographic shapes and standardized concepts
- Requires re-transformation after mapping

#### Data Verification

**Completeness Checks**

- Compare observation count with CSV line count
- Page through generated observations
- Verify all data was converted correctly

**Quality Checks**

- Test links to concept tables
- Verify multilingual content (switch language in top right)
- Check metadata completeness for all languages
- Validate dimension mappings

### Step 4: Publication

**Purpose**: Publish the completed cube to public databases and platforms.

#### Pre-Publication Checklist

- ✅ Verify all data and metadata accuracy
- ✅ Confirm publication status (draft/published)
- ✅ Set publication targets (visualize.admin.ch, opendata.swiss)
- ✅ Ensure non-sensitive data only

⚠️ **Warning**: For visualize.admin.ch republishing, maintain cube structure to avoid breaking existing visualizations.

#### Publication Process

1. **Start Publication**

   - Click "Start publication" button
   - Monitor job in "Previous publications" list
   - Wait for green status indicator
2. **Verify Publication**

   - Check availability on target platforms
   - Test cube functionality in visualize.admin.ch
   - Confirm metadata appears on opendata.swiss
   - Run the provided SPARQL query by cube creator in LINDAS

#### Publication Management

**Version Control**

- Each publication creates a complete new version
- Previous versions marked as expired automatically
- Old versions remain accessible for compatibility

**Management Actions**

- **Expired**: Automatic flag for superseded versions
- **Unlist**: Makes cube unavailable (reversible by republishing)
- **Delete**: Manual database removal (irreversible)

## Best Practices

### Data Preparation

- Use consistent delimiters across all CSV files
- Validate CSV syntax before upload
- Keep backup copies of original data
- Document data transformations and decisions

### Mapping Strategy

- Start with sample data for complex cubes
- Use meaningful identifier templates
- Link to Shared Dimensions when appropriate
- Maintain consistent naming conventions

### Metadata Quality

- Provide descriptions in all relevant languages
- Use specific, descriptive dimension names
- Choose appropriate scales of measure
- Include units for all measurements

### Publication Management

- Test with draft status before publishing
- Maintain cube structure for existing visualizations
- Document changes between versions
- Monitor platform availability after publication

## Troubleshooting

### Common Upload Issues

- **Encoding Problems**: Convert files to UTF-8
- **Syntax Errors**: Use CSV validation tool
- **Empty Lines**: Remove all empty rows

### Transformation Failures

- **Type Mismatches**: Check data format against selected types
- **Missing Values**: Set appropriate default values
- **Invalid Characters**: Review identifier templates

### Publication Issues

- **Missing Metadata**: Complete all required fields
- **Platform Unavailability**: Check platform status and configuration
- **Visualization Errors**: Verify cube structure and metadata completeness

### Getting Help

- Check transformation logs for detailed error messages
- Use the cube-checker tool for visualize.admin.ch cubes
- Review the [official wiki](https://github.com/zazuko/cube-creator/wiki) for detailed documentation
- Submit issues to the [GitHub repository](https://github.com/zazuko/cube-creator/issues)

---

_This guide covers the essential workflow for using Cube Creator. For advanced features and specific use cases, consult the [official documentation](https://github.com/zazuko/cube-creator/wiki)._
