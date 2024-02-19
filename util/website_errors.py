
class Error:
    def __init__(self, err_class: str, err_code: int, err_type: str, info: str) -> None:
        self.cls = err_class # Letter that describes error type
        self.code = err_code # Number of specific error
        self.type = err_type # Type of error - Where's the problem?
        self.info = info # Explanation about the error

    @property
    def title(self):
        return f"Error {self.cls}/{self.code} : {self.type}"


# Request Errors
class RequestError(Error):
    err_class = "R"
    err_type = "Invalid Request"

    def __init__(self, err_code, err_info) -> None:
        super().__init__(RequestError.err_class, err_code, RequestError.err_type, err_info)


class InvalidRequestError(RequestError):
    err_code = 1
    err_info = "This request is not a valid request."

    def __init__(self) -> None:
        super().__init__(InvalidRequestError.err_code, InvalidRequestError.err_info)


# Resource Errors
class ResourceError(Error):
    err_class = "S"
    err_type = "Invalid Resource Requested"

    def __init__(self, err_code, err_info) -> None:
        super().__init__(ResourceError.err_class, err_code, ResourceError.err_type, err_info)


class UnexistingResourceError(ResourceError):
    err_code = 1
    err_info = "This resource does not exist."

    def __init__(self) -> None:
        super().__init__(UnexistingResourceError.err_code, UnexistingResourceError.err_info)


class AcessDeniedResourceError(ResourceError):
    err_code = 2
    err_info = "Access denied. You don't have permition to access this resource."

    def __init__(self) -> None:
        super().__init__(AcessDeniedResourceError.err_code, AcessDeniedResourceError.err_info)

print(UnexistingResourceError().title)