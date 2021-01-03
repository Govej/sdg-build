# -*- coding: utf-8 -*-

import frictionless

class DataSchemaInputBase:
    """A base class for importing a data schema, querying it, and validating with it.

    This class assumes imported schema are valid Table Schema.
    See here: https://specs.frictionlessdata.io/table-schema/
    """


    def __init__(self, source=None):
        """Create a new DataSchemaInputBase object."""

        self.source = source
        self.schema = self.load_all_schema()


    def load_all_schema(self):
        """Load the schema for all indicators. This should be overridden by a subclass."""
        raise NotImplementedError


    def get_schema_for_indicator(self, indicator):
        indicator_id = indicator.inid
        if indicator_id in self.schema and self.schema[indicator_id] is not None:
            return self.schema[indicator_id]
        return None


    def validate(self, indicator):
        """Validate the data for an Indicator object.

        Parameters
        ----------
        indicator : Indicator
            The instance of Indicator to validate

        Returns
        -------
        boolean
            True if validation passes, False otherwise
        """
        status = True
        if indicator.has_data():
            df = indicator.data
            schema = self.get_schema_for_indicator(indicator)
            if schema is not None:
                report = frictionless.validate.validate_table(df, schema=schema)
                # TODO: Output some feedback of errors.
                status = report.valid()

        return status


    def get_descriptor(self, indicator):
        return dict(self.get_schema_for_indicator(indicator))
