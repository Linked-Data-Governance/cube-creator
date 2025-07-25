# Example of a transformation in Cube Creator

First make sure you have read the [user guide on cube creator](./README.md).

## Data

For this example, we will use the [\_710_CHdipl_excel_de.csv](./_710_CHdipl_excel_de.csv) data, which is an analysis made by OBSAN from the following databases : Medical Professions Register (MedReg), FSO – Database of students and degrees of the Swiss Higher Education Information System (SHIS-studex).

The data is about the number of degrees earned by students between 2013 and 2023.

To be able to transform the CSV data into RDF cube, we need to have a clean CSV who meets Cube Creator requirements. So we will use the file [data_clean.csv](./data_clean.csv).

By looking at the data, we can have a concept table, who will be used to translate the degrees in differents languages (de, fr, en, it). The file [degree_concept.csv](./degree_concept.csv) contains the translation of all the degrees listed in [data_clean.csv](./data_clean.csv).

## Transformation in Cube Creator

After creating the project in Cube Creator, you can load the 2 CSV files : [data_clean.csv](./data_clean.csv) and [degree_concept.csv](./degree_concept.csv).

Now follow these steps (Cube Creator interface provide the main steps - 1. CSV Mapping, 2. Transformation, 3. Cube Designer and 4. Publication):

1. From [data_clean.csv](./data_clean.csv), create the Cube Table by selecting all the dimensions that will be part of the generated RDF cube (don't choose the colum _*degree*_, because we will create a link to the concept table). Click on "Create table from selected columns" and select the checkbox "Cube table"
2. For each dimension add his metadata
3. From [degree_concept.csv](./degree_concept.csv), create the Concept Table and mention the target property `schema:name` and the corresponding language tag for each column. For instance for the column `degree_de` the language tag will be _*de*_
4. Click on the "+" button from the cube table, then click on "Link to another table" and create the property _degree_ to link the cube table to the concept table. If the identifier template of the concept table is `Degree/{degree_de}`, he will take its values from the column _*degree*_ of [data_clean.csv](./data_clean.csv) for `{degree_de}`. By doing this, we will have for instance an URI that contains `Degree/Diplome` which represents the URI of the corresponding concept. All the values of the columns _*degree*_ will be a resource that refer to a concept which have a predicate/property `schema:name` whose values correspond to the translation of _*Diplome*_ in french, english, german and italian.
5. Go to the tab "2. Transformation" and click on "Start transformation" after the mapping completion
6. Go to the tab "3. Cube Designer" and add metadata on the cube. Each dimension must have a dimension type and a scale of measure. Add the dimension name in differents languages and mention the corresponding language tag. For the _*year*_, we can link his values to the Shared Dimension _*Year/Année*_ which already exists on LINDAS. You can see an overview of the existing shared dimensions by running the following query on LINDAS sparql endpoint ([https://lindas.admin.ch/sparql/](https://lindas.admin.ch/sparql/)):

```sql
PREFIX schema: <http://schema.org/>

SELECT * WHERE {
  ?shared_dimension a <https://cube.link/meta/SharedDimension>;
  	schema:name ?name.
  FILTER(lang(?name) = "en")
}
```

7. To be able to download the RDF graph in turtle and query the data on LNDAS, you must go to the tab "4. Publication" and click on "Start publication". But before that, make sure that you've added the platform where you want to publish the data (e.g visualize.admin.ch) and fill the required metadata fields for the cube itself
