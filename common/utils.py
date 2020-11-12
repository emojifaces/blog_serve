from rest_framework.response import Response


class APIResponse(Response):
    """
    自定义response
    status: 1 成功
            0 失败
    msg: ok 成功
         err 失败
    """

    def __init__(self, data_status, data_msg='', data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        return_data = {
            'status': data_status,
            'msg': data_msg
        }
        if data:
            return_data['data'] = data
        return_data.update(kwargs)
        super().__init__(data=return_data, status=status,
                         template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)
