# TODO

## Security / Auth

- [ ] **Once we have a domain (HTTPS), replace `is_secure` with `is_production` in `app/routes/auth.py`**

  Currently the `Secure` cookie flag is **protocol-adaptive** (`is_secure = request.url.scheme == "https"`) so authentication works over plain HTTP on the current EC2 server.

  Once the API is served over HTTPS behind a real domain, the `Secure` flag should be forced on in production by reverting to the environment-based check:

  ```python
  is_production = settings.ENVIRONMENT == "production"
  secure=is_production
  ```

  This applies to both the `login` cookie set and the `logout` cookie delete in `app/routes/auth.py`.