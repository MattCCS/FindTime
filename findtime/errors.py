
class Error(Exception): pass

class ParsingError(Error): pass
class NoTimesError(ParsingError): pass
class BadTimeError(ParsingError): pass  # <3 sans
class BadPeriodError(ParsingError): pass
class BadDayRangeError(ParsingError): pass

class ValidationError(Error): pass
class TimeValidationError(ValidationError): pass
class DayValidationError(ValidationError): pass
class DateValidationError(ValidationError): pass
