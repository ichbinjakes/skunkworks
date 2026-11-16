/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package org.example.polaris;

import io.quarkus.security.identity.SecurityIdentity;
import io.smallrye.common.annotation.Identifier;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.Set;
import org.apache.polaris.service.auth.DefaultAuthenticator;
import org.apache.polaris.service.auth.external.mapping.PrincipalRolesMapper;

/**
 * A {@link PrincipalRolesMapper} that activates every principal role the authenticated principal
 * has been granted in Polaris.
 *
 * <p>Identity (who the user is) is established by the external IdP (Dex) and resolved to a Polaris
 * principal by {@code org.apache.polaris.service.auth.external.mapping.PrincipalMapper}. Role
 * membership, however, lives only in Polaris' metastore (the grants created during bootstrap), not
 * in the IdP. Returning the single pseudo-role {@link DefaultAuthenticator#PRINCIPAL_ROLE_ALL}
 * instructs {@link DefaultAuthenticator} to activate all of the principal's granted roles, so no
 * role names need to be duplicated in Dex.
 */
@ApplicationScoped
@Identifier("delegate-all")
public class DelegatingPrincipalRolesMapper implements PrincipalRolesMapper {

  @Override
  public Set<String> mapPrincipalRoles(SecurityIdentity identity) {
    return Set.of(DefaultAuthenticator.PRINCIPAL_ROLE_ALL);
  }
}