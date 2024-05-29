from fastapi import APIRouter, status, Depends, HTTPException


class Result:
    """
    The APIResult class defines a generic outcome of a service operation. In case the operation is
    successful, the outcome (or "value") is returned contained within the value attribute of the instance.
    In case of a custom app exception, the service result instance contains information about the
    raised exception (e.g., which status code should be returned to the client).
    """
    def __init__(self, success, value, error):
        self.success = success
        self.error = error
        self.value = value

    @property
    def failure(self):
        """True if operation failed, False if successful (read-only)."""
        return not self.success

    def __str__(self):
        if self.success:
            return f'[Success]'
        else:
            return f'[Failure] "{self.error}"'

    def __repr__(self):
        if self.success:
            return f"<Result success={self.success}>"
        else:
            return f'<Result success={self.success}, message="{self.error}">'

    @classmethod
    def fail(cls, error):
        """Create a Result object for a failed operation."""
        return cls(False, value=None, error=error)

    @classmethod
    def ok(cls, value=None):
        """Create a Result object for a successful operation."""
        return cls(True, value=value, error=None)

    @property
    def items(self):
        """Create a Result object for a successful operation"""
        if self.failure:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        return self.value

    @property
    def item(self):
        """Create a Result object for a successful operation."""
        if self.failure:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(self.error))
        return self.value
